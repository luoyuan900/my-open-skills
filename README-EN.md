# My Open Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-blue)](https://agentskills.io)

A personal collection of [Agent Skills](https://agentskills.io) for Claude Code and other AI coding assistants. Covers end-to-end novel writing — from ideation to chapter-by-chapter production — as well as AI video prompt engineering (MiniMax H3) and a local ComfyUI render-and-canvas workflow.

## Skills Overview

| Skill | Role | Core Capability |
|-------|------|----------------|
| [novel-generator](./novel-generator/) | Production Writer | Chapter-by-chapter web-novel generation, memory system for consistency, pacing formulas |
| [novel-writer-cn](./novel-writer-cn/) | Planning Editor | Deep character/worldbuilding design, multi-genre writing techniques |
| [novel-orchestrator](./novel-orchestrator/) | Orchestrator | Coordinated workflow, quality control for long-form, escalation decisions |
| [h3-prompt-writing](./h3-prompt-writing/) | Video Prompt Engineer | MiniMax H3 multimodal video prompts: structured writing for T2VA/I2VA/FL2VA/L2VA/Ref2VA |
| [local-miora-canvas](./local-miora-canvas/) | Local Render × Canvas | Local ComfyUI image/video generation + Miora canvas asset board and delivery |

## Quick Install

Copy the desired skill directory to `~/.claude/skills/`:

```bash
# Clone the repo
git clone https://github.com/luoyuan900/my-open-skills.git

# Install all skills
cp -r my-open-skills/novel-generator ~/.claude/skills/
cp -r my-open-skills/novel-writer-cn ~/.claude/skills/
cp -r my-open-skills/novel-orchestrator ~/.claude/skills/
cp -r my-open-skills/h3-prompt-writing ~/.claude/skills/
cp -r my-open-skills/local-miora-canvas ~/.claude/skills/
```

Or install only the ones you need.

## Use Cases

### 🚀 Fast Web-Novel Production → novel-generator

For Chinese web-novel genres (cultivation, rebirth, system-flow) with clear direction and daily update cadence.

```
"Help me write a cultivation novel about a useless young man who gets an alchemy system and rises to the top"
```

- Auto-completes writing prompts → generates outline → chapter-by-chapter writing
- 2,000-3,000 words per chapter, every chapter has satisfying moments
- `.learnings/` memory system maintains character, location, and plot consistency

### 🎨 Deep Craft / Non-Web-Novel → novel-writer-cn

For sci-fi, mystery, romance, wuxia, or when you need detailed character design and worldbuilding.

```
"Help me design the faction landscape of a cyberpunk world"
"Continue writing this story with one more chapter"
```

- Three-act structure, Hero's Journey, and other classic frameworks
- Professional templates: character cards, world bible, chapter planner
- Multi-genre writing guides

### 🏗️ Epic Long-Form → novel-orchestrator

For novels over 20 chapters that need both literary depth and web-novel pacing.

```
"Help me write a 40-chapter fantasy epic about a mortal rising to godhood"
```

- Planning phase: novel-writer-cn for deep design
- Production phase: novel-generator for efficient writing
- Polish phase: novel-writer-cn for quality refinement

### 🎬 AI Video Prompts → h3-prompt-writing

For multimodal video generation with MiniMax H3, when you need to rewrite a one-line brief into a structured English prompt.

```
"Rewrite this storyboard into an H3 Ref2VA six-section prompt"
"Use I2VA mode to continue 15 seconds forward from this first frame"
```

- Covers all five modes: T2VA / I2VA / FL2VA / L2VA / full-reference Ref2VA
- Base modes use `integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music`
- Full-reference mode uses `subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`
- Pure local readable files, no external API dependency, portable to any Agent Skills-compatible agent

### 🖼️ Local Render & Canvas → local-miora-canvas

Local ComfyUI (127.0.0.1:8818) image/video generation, with a Miora canvas to centrally manage art assets and segmented clips.

```
"Generate this character set with krea2 and register them on the canvas"
"Use the canvas character sheets as references to render segmented videos with the H3 r2v template"
```

- krea2 direct 1024 output, positive-only prompts, batch queueing to reduce reloads
- MiniMax H3 with 8-step acceleration LoRA, 0.5MP, 17k+5 frame-length formula
- Canvas is asset board + delivery panel only; cloud generation channels are forbidden
- Hard VRAM limit: RTX 3060 12GB must not be exceeded

## Skill Selection Guide

```
Is it a web-novel genre (cultivation/rebirth/system)?
  ├─ Yes → Clear direction? → novel-generator
  │        └─ Vague / want depth / want originality → novel-orchestrator
  └─ No → novel-writer-cn

Design-only tasks (character/world/outline) → novel-writer-cn
Editing or polishing existing chapters → novel-writer-cn
Long-form (>20 chapters) with quality focus → novel-orchestrator
```

## Project Structure

```
my-open-skills/
├── README.md
├── novel-generator/           # Web-novel generator
│   ├── SKILL.md               # Main workflow
│   ├── assets/                # Templates
│   ├── .learnings/            # Memory system
│   ├── references/            # Reference guides
│   ├── scripts/               # Init scripts
│   └── output/                # Chapter output
├── novel-writer-cn/           # Novel writing assistant
│   ├── SKILL.md               # Main workflow
│   ├── assets/templates/      # Professional templates
│   └── references/            # Writing guides
├── novel-orchestrator/        # Orchestrator
│   └── SKILL.md               # Collaboration workflow
├── h3-prompt-writing/         # H3 video prompt engineer
│   ├── SKILL.md               # Main workflow
│   ├── agents/                # OpenAI/Codex UI metadata
│   └── references/            # base-en / ref-en prompt structure guides
└── local-miora-canvas/        # Local render × canvas asset management
    ├── SKILL.md               # Main workflow
    ├── references/            # Node-level workflow definitions
    └── scripts/               # ComfyUI submit/monitor scripts
```

## Compatibility

Compatible with tools supporting the Agent Skills specification:

- **Claude Code** — Place in `~/.claude/skills/`
- **Cursor** — Place in project `skills/` directory
- **OpenAI Codex / GitHub Copilot** — Follows Agent Skills spec

> **Note**: The skill documentation and templates are primarily in Chinese (zh-CN), as they are designed for Chinese novel creation.

## License

[MIT](LICENSE)
