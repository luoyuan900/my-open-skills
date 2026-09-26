# My Open Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-blue)](https://agentskills.io)

个人使用的 [Agent Skills](https://agentskills.io) 集合。

## 技能一览

| 技能 | 定位 | 核心能力 |
|------|------|---------|
| [novel-generator](./novel-generator/) | 量产写手（其他开源） | 爽文逐章生成、记忆防穿帮、节奏公式 |
| [novel-writer-cn](./novel-writer-cn/) | 策划编辑（其他开源） | 深度角色/世界观设计、多类型写作技巧 |
| [novel-orchestrator](./novel-orchestrator/) | 编排调度（自己写的） | 两者协同、长篇质量控制、降级决策 |
| [h3-prompt-writing](./h3-prompt-writing/) | 视频提示词工程（自己写的） | MiniMax H3 多模态视频提示词：T2VA/I2VA/FL2VA/L2VA/Ref2VA 结构化撰写 |
| [local-miora-canvas](./local-miora-canvas/) | 本地出片 × 画布（自己写的） | 本地 ComfyUI 出图/出视频 + Miora 画布资产看板与交付 |

## 快速安装

将需要的技能目录复制到 `~/.claude/skills/`：

```bash
# 克隆仓库
git clone https://github.com/luoyuan900/my-open-skills.git

# 安装全部技能
cp -r my-open-skills/novel-generator ~/.claude/skills/
cp -r my-open-skills/novel-writer-cn ~/.claude/skills/
cp -r my-open-skills/novel-orchestrator ~/.claude/skills/
cp -r my-open-skills/h3-prompt-writing ~/.claude/skills/
cp -r my-open-skills/local-miora-canvas ~/.claude/skills/
```

也可只安装你需要的那个。

## 使用场景

### 🚀 快速量产爽文 → novel-generator

想写都市修仙/重生逆袭/系统流爽文，方向明确，保持日更。

```
"帮我写一个废柴少年获得炼丹系统后逆袭的修仙爽文"
```

- 自动补全提示词 → 生成大纲 → 逐章创作
- 每章 2000-3000 字，章章有爽点
- `.learnings/` 记忆系统自动维护角色、地点、情节一致性

### 🎨 深度创作/非爽文 → novel-writer-cn

写科幻/悬疑/言情/武侠，或需要精细的角色设计、世界观构建。

```
"帮我设计一个赛博朋克世界的势力分布"
"给这个故事续写一章"
```

- 三幕/英雄之旅等经典结构
- 角色卡、世界圣经等专业模板
- 多类型写作指导

### 🏗️ 长篇大作 → novel-orchestrator

20 章以上的长篇，想要既有深度又是爽文节奏。

```
"帮我写一部40章的玄幻长篇，主角从凡人一步步登顶"
```

- 策划期用 novel-writer-cn 深度设计
- 量产期用 novel-generator 高效写作
- 润色期用 novel-writer-cn 精修质量

### 🎬 AI 视频提示词 → h3-prompt-writing

用 MiniMax H3 做多模态视频生成，需要把一句话需求改写成结构化的英文提示词。

```
"帮我把这段分镜写成 H3 的 Ref2VA 六段式提示词"
"用 I2VA 模式，从这张首帧图往下续写 15 秒"
```

- 覆盖 T2VA / I2VA / FL2VA / L2VA / 全参考 Ref2VA 五种模式
- 基础模式走 `integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music` 三段式
- 全参考模式走 `subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music` 六段式
- 纯本地可读文件，无外部 API 依赖，可移植到任意支持 Agent Skills 的 agent

### 🖼️ 本地出片与画布管理 → local-miora-canvas

本地 ComfyUI（127.0.0.1:8818）出图/出视频，并用 Miora 画布集中管理美术资产与分段成片。

```
"用 krea2 出这套角色定妆图，登记到画布"
"以画布上的定妆图为参考，用 H3 r2v 模板出分段视频"
```

- krea2 直出 1024、纯正向 prompt、同模型 batch 进队减少 reload
- MiniMax H3 用 8 步加速 LoRA、0.5MP、17k+5 帧长公式
- 画布只做资产看板与交付面板，禁止云端生成通道
- 显存硬约束：RTX 3060 12GB 不得击穿

## 技能选择速查

```
是爽文题材吗?
  ├─ 是 → 有明确方向? → novel-generator
  │       └─ 方向模糊/要深度/不套路 → novel-orchestrator
  └─ 否 → novel-writer-cn

只做设计（角色/世界观/大纲）→ novel-writer-cn
润色修改已有章节 → novel-writer-cn
长篇(>20章)追求品质 → novel-orchestrator
```

## 项目结构

```
my-open-skills/
├── README.md
├── novel-generator/           # 爽文生成器
│   ├── SKILL.md               # 主工作流
│   ├── assets/                # 模板
│   ├── .learnings/            # 记忆系统
│   ├── references/            # 参考指南
│   ├── scripts/               # 初始化脚本
│   └── output/                # 章节输出
├── novel-writer-cn/           # 小说写作助手
│   ├── SKILL.md               # 主工作流
│   ├── assets/templates/      # 专业模板
│   └── references/            # 写作指南
├── novel-orchestrator/        # 编排调度器
│   └── SKILL.md               # 协作流程
├── h3-prompt-writing/         # H3 视频提示词工程
│   ├── SKILL.md               # 主工作流
│   ├── agents/                # OpenAI/Codex UI 元数据
│   └── references/            # base-en / ref-en 提示词结构指南
└── local-miora-canvas/        # 本地出片 × 画布资产管理
    ├── SKILL.md               # 主工作流
    ├── references/            # 节点级工作流定义
    └── scripts/               # ComfyUI 提交/监控脚本
```

## 兼容性

兼容支持 Agent Skills 规范的工具：

- **Claude Code** — 放入 `~/.claude/skills/`
- **Cursor** — 放入项目 `skills/` 目录
- **OpenAI Codex / GitHub Copilot** — 遵循 Agent Skills 规范

## 许可证

[MIT](LICENSE)
