# My Open Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-blue)](https://agentskills.io)

个人的 [Agent Skills](https://agentskills.io) 集合，用于 Claude Code 等 AI 编程助手。提供小说创作的全流程支持——从灵感构思到逐章量产，覆盖角色设计、世界观构建、爽文节奏、记忆防穿帮等。

## 技能一览

| 技能 | 定位 | 核心能力 |
|------|------|---------|
| [novel-generator](./novel-generator/) | 量产写手 | 爽文逐章生成、记忆防穿帮、节奏公式 |
| [novel-writer-cn](./novel-writer-cn/) | 策划编辑 | 深度角色/世界观设计、多类型写作技巧 |
| [novel-orchestrator](./novel-orchestrator/) | 编排调度 | 两者协同、长篇质量控制、降级决策 |

## 快速安装

将需要的技能目录复制到 `~/.claude/skills/`：

```bash
# 克隆仓库
git clone https://github.com/luoyuan900/my-open-skills.git

# 安装全部技能
cp -r my-open-skills/novel-generator ~/.claude/skills/
cp -r my-open-skills/novel-writer-cn ~/.claude/skills/
cp -r my-open-skills/novel-orchestrator ~/.claude/skills/
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
└── novel-orchestrator/        # 编排调度器
    └── SKILL.md               # 协作流程
```

## 兼容性

兼容支持 Agent Skills 规范的工具：

- **Claude Code** — 放入 `~/.claude/skills/`
- **Cursor** — 放入项目 `skills/` 目录
- **OpenAI Codex / GitHub Copilot** — 遵循 Agent Skills 规范

## 许可证

[MIT](LICENSE)
