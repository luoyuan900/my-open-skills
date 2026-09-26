# 工作流节点定义参考

本文档记录两个本地 ComfyUI workflow 模板的节点级操作要点。模板文件在用户机器上：
`C:/Users/luo/Downloads/comfyuiapi/`。加载本 skill 后按需读取本文档，避免每次重推节点 id。

## 一、krea2 图像 workflow（Krea2_samll_then_large.json）

模型栈：krea2_turbo fp8 UNET + qwen3vl_4b CLIP（type 必须为 `krea2`）+ qwen_image_vae。
采样：euler 8 步，cfg=1，负向通道走 ConditioningZeroOut（不生效，prompt 必须纯正向）。

### 关键节点操作

| 节点 | 作用 | 操作 |
|---|---|---|
| EmptyLatentImage | 出图尺寸 | **写字面量** `width`/`height`，绕开 ResolutionSelector（其枚举不出现在 object_info，POST 会报错） |
| UNETLoader (30:10) | krea2_turbo fp8 | KSampler 的 model **直接接本节点**（LoRA 已摘除，见下） |
| KSampler | 采样 | seed 用 `noise_seed`，统一 20260816 |
| SaveImage (29) | 保存图像 | filename_prefix 已清理为 `krea2_1024`；提交时按项目覆盖为版本化命名 |

**LoRA 与放大分支均已移除（2026-09-26）**：模板原带 glowing-amber-linework LoraLoaderModelOnly + 模型开关，已删节点并把 KSampler 直连 UNETLoader；RealESRGAN 放大分支（UpscaleModelLoader/ImageScaleToTotalPixels/ImageUpscaleWithModel/第二个 SaveImage）已整体摘除，**现在只有单一 1024 直出输出**。备份：`Krea2_samll_then_large.backup-lora.json`（LoRA 版）、`Krea2_samll_then_large.backup-upscale.json`（含放大分支版）。模板中残留的 PrimitiveBoolean"Enable LoRA?"仅喂 prompt 拼接开关（false=直用原文），不影响任何链路。

### 分辨率（直出 1024，不放大）

| 画幅 | 宽 × 高 |
|---|---|
| 1:1 | 1024 × 1024 |
| 16:9 | 1024 × 576 |
| 2:3 竖 | 704 × 1056 |
| 3:2 横 | 1056 × 704 |

产物命名约定：`<编号>_<资产名>_00001_.png`（编号 01=主角, 02=主机体, 03/03b=敌方双形态, 04=场景A, 05=场景B…）。

## 二、MiniMax H3 视频 workflow（video_minimax_h3_r2v_turbo_8_step.json）

模型栈：MiniMaxH3TurboLoRA（larryvrh 加速 LoRA，8 步实跑）+ qwen3vl CLIP。

### 关键节点映射（以 v8 实测为准）

| 节点 id | 作用 | 操作 |
|---|---|---|
| `136` | r2v 参考图 autogrow | 扁平点号键：`wf["136"]["inputs"]["ref_images.ref_image_2"] = ["144", 0]`；ref_image_0/1 走各自 LoadImage 节点再连线 |
| `137` / `139` / `144` | LoadImage ×3 | `inputs.image` 传入 `/upload/image` 返回的文件名；对应 prompt 里 `<Picture 1/2/3>` |
| `138` | prompt | 六段式英文 prompt（见 h3-prompt-writing skill） |
| `132` | 时长（秒） | 写整数秒；帧数由内部公式换算（17k+5） |
| `129` | noise_seed | 统一 20260816 |
| `92` | filename_prefix | 版本化命名，如 `video/mecha_S4_v8_local` |

### 帧长公式与上限

```
frames = max(5, round(dur_s * 24))
frames += (5 - frames % 17) % 17      # 对齐 17k+5
```

| 时长 | 帧数 |
|---|---|
| 5s | 125 |
| 8s | 197 |
| 10s | 243 |
| 15s | 362（H3 训练上限，勿超） |

### 分辨率（0.5MP，绕开 ResolutionSelector 写字面量）

| 画幅 | 宽 × 高 | 说明 |
|---|---|---|
| 16:9 | 960 × 544 | 主用；两者均为 16 倍数 |
| 2:3 竖 | 608 × 912 | 竖构图短片 |
| 1:1 | 704 × 704 | 方图素材 |

### prompt 结构速查

- 六段：`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`（无 BGM 时 music 写 N/A）。
- 多镜头：每段 `[Shot N] At MM:SS` 标切口 → H3 会真实切镜头。
- 一镜到底：**只写一个 `[Shot 1]`** + "There are no cuts: one continuous ..."，事件用 "Around 00:04 / 00:07 / 00:10" 标记在同一连续运镜叙述内。
- 声音写进 `overall_soundscape`（机械声/吼叫等环境声）；音乐类需求不属于本 skill（本地出片默认无 BGM）。

## 二b、MiniMax H3 首帧续接 workflow（video_minimax_h3_fl2v_turbo_8step.json）

> **注意节点 id 差异**：r2v 模板（r2v_turbo_8_step）的生成节点是 `136`（MiniMaxH3ReferenceToVideo，宽高/时长在此节点覆盖），prompt 在 `138`；fl2v 模板的生成节点是 `131`（MiniMaxH3ImageToVideo，prompt/width/height/length 全在此节点）。两个模板的 SaveVideo 都是 `92`、seed 都是 `129`，但其余 id 不通用——改模板前先 dump 节点图确认。

用途：续接上一段的尾帧（场景接续）。与 r2v 的区别：**无参考图，只有 first_frame**，prompt 里不写 `<Picture N>`，主体全靠文字描述 + 首帧锚定。

| 节点 id | 作用 | 操作 |
|---|---|---|
| `131` | MiniMaxH3ImageToVideo | prompt/width/height/length 都在此节点；`first_frame` 是 **optional 输入，模板默认没接**——需自补 LoadImage 节点（如 `"200"`）并连 `wf["131"]["inputs"]["first_frame"] = ["200", 0]`；宽高写字面量覆盖 115（注意该节点尺寸步进为 32：864/480 均合法） |
| `129` | noise_seed | 写 seed |
| `92` | filename_prefix | 版本化命名 |
| `132`/`133` | 时长数学节点 | 直接把 `131.length` 写字面量（17k+5 帧数，如 243=10s），绕开表达式节点 |
| `127`/`134` | UNET (fl2va_pruned_int8) + TurboLoRA | 模板已接好，勿动 |

尾帧抽取：`ffmpeg -sseof -0.05 -i 上一段.mp4 -frames:v 1 -q:v 1 首帧.png`。

## 三、提交与监控协议

使用 `scripts/comfy_submit.py`：

```python
import sys; sys.path.insert(0, "<skill_dir>/scripts")
from comfy_submit import upload, submit, wait_for, load_template

wf = load_template(r".../video_minimax_h3_r2v_turbo_8_step.json")
wf = wf / 深拷贝防污染 / 填节点
name = upload(r"path/to/ref.png")          # POST /upload/image
pid = submit(wf, client_id="mecha_s4")     # POST /prompt, 校验 node_errors, 返回 prompt_id
fname = wait_for(pid, timeout=2700)        # 每 30s GET /history/{pid}, 返回产物文件名
```

硬性规则：

1. `submit` 响应含 `node_errors` → 立即失败退出，不进监控。
2. 监控只认 prompt_id；`status_str=error` → 打印 status 摘要后退出。
3. 文件落盘判据：history outputs 中出现 `.mp4` / `.png` 条目；稳妥起见再查文件 size 稳定（间隔 5s 两次一致）。
4. 进队前 `GET /queue` 检查 running/pending，用户可能手动占了卡。
