---
name: local-miora-canvas
description: 本地 ComfyUI 出片流水线的资产管理 skill。当用户要"在本地生成图片/视频并用画布集中管理美术资源"、"用 miora 画布管理资产"、"krea2 出图 + MiniMax H3 出视频"、"本地 comfyui 出片"时使用。核心约定：krea2 直出 1024 不放大、纯正向 prompt；MiniMax H3 用 8 步加速 LoRA、0.5MP、17k+5 帧长；Miora 画布（.miora）只做资源看板与交付面板，禁止云端生成通道。触发词：画布管理美术资源、本地出图、本地出视频、krea2、H3、miora 画布、资产看板。
agent_created: true
---

# Local Miora Canvas — 本地出片 × 画布资产管理

## 职责边界

- **Miora 画布（.miora）= 资产看板 + 交付面板**：登记角色/场景/道具参考图与分段视频，按镜头/资产分区排列，供用户审阅。
- **生成本体 = 本地 ComfyUI（127.0.0.1:8818）**：图片走 krea2，视频走 MiniMax H3。本 skill 为显式本地限定场景，不调用云端 ImageGen / VideoGen。
- 画布不支持文字条目——所有标注放进条目 `title`，叙述性说明写在回复里。

## 环境配置（首次安装必读）

本 skill **不写死任何机器路径 / URL**。所有路径与地址在运行时按以下优先级解析
（实现见 `scripts/comfy_submit.py`）：

1. 环境变量（最高优先）
2. 同目录 `config.json`（首次安装时由 agent 询问用户后写入，已加入 `.gitignore`，不提交）
3. ComfyUI 服务地址自动探测本机端口 `8818` / `8188`
4. 模板 / 输出目录按文件名在常见目录（Downloads / Documents / AI / ComfyUI）自动查找
5. 仍找不到 → 脚本抛清晰错误，agent 询问用户并把绝对路径写进 `config.json`

### 需要配置的项

| 配置键 | 环境变量 | 含义 | 兜底 |
|---|---|---|---|
| `comfyui_url` | `COMFYUI_URL` | ComfyUI 服务地址 | 自动探测 8818 / 8188 |
| `krea2_template` | `KREA2_TEMPLATE` | krea2 图像 workflow JSON 绝对路径 | 按文件名自动查找 |
| `h3_r2v_template` | `H3_R2V_TEMPLATE` | H3 r2v 视频 workflow JSON 绝对路径 | 按文件名自动查找 |
| `h3_fl2v_template` | `H3_FL2V_TEMPLATE` | H3 fl2v 视频 workflow JSON 绝对路径 | 按文件名自动查找 |
| `output_dir` | `COMFYUI_OUTPUT` | ComfyUI 产出落盘目录（与 ComfyUI 同机的本地路径） | **必须显式配置** |

### 首次安装流程（agent 执行）

1. 探测 `http://127.0.0.1:8818` 与 `8188` 能否连通；命中即用，无需配置。
2. 向用户询问四个本地路径：krea2 模板、H3 r2v 模板、H3 fl2v 模板、ComfyUI 输出目录。
3. 把结果写入 `local-miora-canvas/config.json`（参考 `config.example.json`，不要提交进 git）。

> 不想维护 `config.json` 也可以：直接给运行环境设环境变量，或把模板放进 Downloads
> 等常见目录让其按文件名自动发现。`output_dir` 无法自动探测，务必显式给。

## 固定约定（与机器无关）

| 项 | 值 |
|---|---|
| 统一 seed | `20260816` |
| 显存上限 | RTX 3060 12GB，不得击穿 |
| 提交/监控脚本 | 本 skill `scripts/comfy_submit.py` |

节点级工作流定义（node id 映射、分辨率表、帧长公式）见 `references/workflows.md`。

## 流水线

1. **资产 prompt 定义**：用 `cinematic-asset-prompts` 拆解剧本 → 角色定妆/场景空镜/道具设定图清单。krea2不吃负向语义，所有 prompt **纯正向描述**，排除项改用锚定词（"不是X/无X/禁止X"会被正向编码）。
2. **krea2 出图**：直出 1024，**跳过 ESRGAN 放大环节**。同模型任务 batch 进队（减少模型 reload），见下文 krea2 规则。
3. **画布登记**：出图完成后 `miora_write_canvas`（action=create 首建 / update 增补）把所有资产图铺上画布。
4. **H3 出视频**：以画布上的定妆图为参考图，r2v 模板出分段视频，见下文 H3 规则。
5. **抽帧验证**：出片后抽 4–6 帧验证动作衔接/角色一致性/结尾构图，不合格改 prompt 重跑（改版本号前缀，不覆写旧版）。
6. **画布更新**：验证通过的视频 update 进画布对应槽位；画布接受任意本地 mp4（混合来源已验证）。
7. **交付**：`present_files` 必须带 `.miora` 文件本身（放 files 首位）+ `copied_assets` 里的每条媒体路径；再 `miora_open_canvas` 打开侧栏预览。**禁止把生成工具返回的原始 localPath / signedUrl 直接交给 present_files**——必须用画布回传的 copied_assets。

## krea2 出图规则

- 模板：`Krea2_samll_then_large.json`（krea2_turbo fp8 UNET + qwen3vl_4b CLIP(type=krea2) + qwen_image_vae，8 步 euler，cfg=1）。**LoRA 与 RealESRGAN 放大分支均已摘除**，单一 1024 直出输出（KSampler 直连 UNETLoader）；负向通道走 ConditioningZeroOut（不生效，prompt 必须纯正向）。
- **本 skill 约定直出 1024，不做放大**：宽高绕开 ResolutionSelector（其枚举不暴露 object_info），直接写字面量到 EmptyLatentImage。16:9 用 `1024×576`，2:3 用 `704×1056`，1:1 用 `1024×1024`。
- 模板自带 glowing-amber-linework LoRA，正确路径为 `krea2\glowing-amber-linework.safetensors`；若模板路径陈旧（曾出现过 `krea-2\comfy\...`）必须先修正再提交。
- 提交后立即检查响应里的 `node_errors`——ComfyUI 0.36+ 部分执行会把报错节点下游静默剪除，`status=success` 可能是 6ms 假成功。同时核对 history 的 `outputs_to_execute`。

## MiniMax H3 出视频规则

- 模板：`video_minimax_h3_r2v_turbo_8_step.json`（MiniMaxH3TurboLoRA 加速，8 步实跑）。
- **分辨率 0.5MP**：16:9 用 `960×544`（均为 16 的倍数，≈0.52MP）；竖构图 2:3 用 `608×912`。宽高写字面量，绕开 ResolutionSelector。
- 帧长公式（17k+5）：`frames = max(5, round(时长s × 24))`，再 `frames += (5 - frames % 17) % 17`。例：15s → 362 帧（H3 训练上限），8s → 197 帧。
- 参考图挂载：autogrow 输入用**扁平点号键** `wf["136"]["inputs"]["ref_images.ref_image_2"] = ["144", 0]`，不是嵌套 dict。
- 参考图对应 `<Picture N>` 语法写进 prompt（`<Picture 1>` = 主角色/机甲定妆，`<Picture 2>` = 敌方单位，`<Picture 3>` = 杂兵/次要单位，按资产重要性排序）。
- prompt 结构用 `h3-prompt-writing` 的六段式英文格式（subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music）；自由中文长描述的调度符合度差，勿用。一镜到底 = 单一 `[Shot 1]` + "There are no cuts" + 事件时间点标记（Around 00:04…）。
- 提交后按 **prompt_id** 走 `/history/{pid}` 监控（每 30s），绝不按文件名前缀找文件——改版本前缀后旧监控会误报旧文件为 DONE。

## 画布操作细节

- `miora_write_canvas`：action=create 建新画布（覆盖同名文件），action=update 按 `id` 增补/替换、`remove_item_ids` 删除，未提及条目保留。文件放项目根目录（`<project>/xxx.miora`），不要进 `.workbuddy/` 等点目录。
- items 只收 image/video，`source_path` 用本地绝对路径；宽高留空自动探测真实像素。
- 布局 `grid`（默认 4 列）；素材多时按资产分组、视频单独成区。
- 画布文件被复制进 `<name>_assets/` 目录自包含，拷贝结果在返回值 `copied_assets`。

## 通用坑位

- **同模型 batch 进队**：多个 krea2 出图任务一次排队提交，避免反复 reload。
- **版本化前缀**：每次改 prompt/参数递增前缀（`mecha_S4_v8_local`），不覆写旧产物，便于回滚对比。
- **监控超时**：15s/362 帧约 25–30 分钟，超时上限给足 2700s。
- 用户可能在 ComfyUI GUI 手动跑 job——进队前先查 `/queue` 是否空闲，避免挤占显存。
