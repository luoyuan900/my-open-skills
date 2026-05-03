---
name: novel-orchestrator
description: "编排 novel-generator 和 novel-writer-cn 协同创作。触发：(1) 爽文长篇需要深度角色/世界观设计，(2) 兼顾量产效率与文学质量，(3) 不确定用哪个技能。"
license: MIT-0
metadata:
  author: gavin
  version: "1.0.0"
  language: zh-CN
  category: creative-writing
  tags: "novel, orchestration, chinese"
---
# 小说创作编排器

**novel-writer-cn = 策划+编辑（深度设计、多类型、写作技巧）**
**novel-generator = 写手+校对（爽文量产、记忆防穿帮、节奏公式）**

## 技能选择

| 场景 | 技能 |
|------|------|
| 爽文（都市/修仙/玄幻/重生/系统流）+ 方向具体 | novel-generator |
| 科幻/悬疑/言情/武侠 | novel-writer-cn |
| 只做角色/世界观设计 | novel-writer-cn |
| 润色修改已有章节 | novel-writer-cn |
| 爽文长篇(>20章) / 方向模糊 / 要深度角色 / 要不套路 | **本编排器** |

## 四阶段流程

### 阶段一：策划期 → novel-writer-cn
沟通题材→角色深度设计(character-card)→世界观分层(world-bible)→三幕框架划分卷

### 阶段二：导入期 → 编排器桥接
```
character-card → .learnings/CHARACTERS.md（格式: 名称|等级|位置|状态|关系网）
world-bible   → .learnings/STORY_BIBLE.md
outline 关键节点 → .learnings/PLOT_POINTS.md（格式: 章节|事件|角色|伏笔）
地点列表      → .learnings/LOCATIONS.md（格式: 名称|类型|势力|首次出现章节）
```

### 阶段三：量产期 → novel-generator
提示词补全→大纲对齐三幕框架+爽文公式→逐章生成（每章前读.learnings/，每章后更新）→ERRORS.md跟踪

### 阶段四：润色期 → novel-writer-cn
对照ERRORS.md审查→写作技巧润色（视角/场景/对话/节奏）→角色弧线/世界观矛盾修复

## 质量管控

**每章交叉检查**：
- novel-generator: 小爽点✓ 章末钩子✓ .learnings/一致✓ 节奏公式匹配✓
- novel-writer-cn: 视角一致✓ 对话个性✓ 场景变化✓ 伏笔回收✓
- 交叉: 爽点不毁人设 / 不改世界观规则迎合爽点 / 配角有动机非工具人

**降级决策**：
- ERRORS.md 有 high/critical → 暂停量产→novel-writer-cn修正→回阶段二重导入
- medium 累计>5个 → novel-writer-cn集中修复
- 正常 → 每5章做一次 novel-writer-cn 审核

## 长篇节奏模板（每卷15-20章）

| 章节 | 阶段 | 负责 |
|------|------|------|
| 1-3 | 建置期（第一幕）| novel-writer-cn 把控角色世界观，每章保留爽点钩子 |
| 4-12 | 发展期（第二幕）| novel-generator 爽文公式：1-2章小打脸/3-5章中打脸；第8章中点转折 |
| 13-18 | 高潮期（第三幕）| 第15章卷终决战(novel-generator大高潮)，第18章收尾+下卷钩子 |
