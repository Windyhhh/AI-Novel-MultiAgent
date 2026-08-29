<div align="center">

# AI 小说多智能体写作系统 | AI-Novel-MultiAgent

### The multi-agent AI novel writing system.

A multi-agent framework that plans, writes, polishes and reviews novels collaboratively — with consistent characters, controlled styles, and an editor that actually pushes back.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green)](https://www.langchain.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vuedotjs&logoColor=white)](https://vuejs.org/)

</div>

---

**AI-Novel-MultiAgent** is a multi-agent AI novel writing system. Instead of a single model generating text, a team of specialized agents — planner, writer, editor, character, critic — collaborate through a full pipeline: outline design, world-building, chapter writing, style control, and quality review. It keeps characters consistent across chapters and lets an AI editor reject and revise drafts that don't pass review.

> [!NOTE]
> 这是一个中文友好的多智能体小说创作系统。每个智能体负责创作流程中的一个环节，总控智能体负责协调与调度。

---

## Quickstart

```bash
git clone https://github.com/Windyhhh/AI-Novel-MultiAgent.git
cd AI-Novel-MultiAgent

# 1. Start dependencies
docker-compose up -d postgres redis chroma

# 2. Configure environment
cp .env.example .env
# fill in your LLM API key (OpenAI / Qwen / local model)

# 3. Install backend
cd backend
pip install -r requirements.txt

# 4. Init database
alembic upgrade head
python scripts/init_prompts.py

# 5. Run backend
uvicorn app.main:app --reload --port 8000

# 6. Run frontend
cd ../frontend
npm install
npm run dev
```

Open `http://localhost:5173` for the platform, or `http://localhost:8000/docs` for the API.

---

## Features

- **Multi-agent collaboration** — planner, writer, editor, character, knowledge and critic agents work together through an orchestrated pipeline, not a single prompt.
- **Character consistency** — a character memory system tracks personality, speech style and state, and the character agent verifies each chapter stays on-model.
- **Style control** — switch between xianxia, xuanhuan, urban, historical and sci-fi styles; outline templates for three-act, hero's journey and save-the-cat structures.
- **Self-review loop** — the critic agent scores every chapter; drafts below the threshold are sent back to the editor for revision.
- **Multiple LLM backends** — OpenAI, Qwen, Claude, or a local model behind a unified interface.

---

## Architecture

A single orchestrator coordinates six specialized agents:

```
                        Orchestrator
                              │
        ┌──────────────┬──────┴──────┬──────────────┐
        │              │             │              │
   Planner Agent   Writer Agent  Editor Agent  Critic Agent
        │              │             │              │
   Character Agent ────┴── Knowledge Agent ────────┘
```

The writing pipeline runs in three phases:

1. **Planning** — outline, world-building, characters, chapter plan.
2. **Writing** — per-chapter: context retrieval → scene breakdown → draft → dialogue → description.
3. **Review** — consistency check → logic check → pacing → polish → score (≥ 7.0 or revise).

---

## Project Structure

```
AI-Novel-MultiAgent/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── agents/          # orchestrator, planner, writer, editor, character, critic
│   │   ├── memory/          # character / plot / style memory + vector store
│   │   ├── llm/             # openai, qwen, claude, local backends
│   │   ├── prompts/         # per-agent prompt templates
│   │   ├── api/             # routes
│   │   └── services/        # business logic
│   └── scripts/             # init_prompts, import_novel
├── frontend/                # Vue 3 UI
├── prompts/                 # style / structure / character templates
├── examples/                # sample novel & characters
└── docker-compose.yml
```

---

## 技术实现细节

### 架构概览

项目采用模块化设计，核心目录包括：**agents, docs, examples, integrations, qa, scheduler, utils, web**。

### 关键函数

- `check_environment`, `run_web`, `run_cli`, `create_new_novel`, `continue_existing_novel`

### 技术栈与依赖

**核心框架/库**：PyTorch

**主要 import**：
```python
import os
import sys
import argparse
from dotenv import load_dotenv
from web.app import run_app
from agents import OutlineAgent, ChapterPlanningAgent, ContentGenerationAgent
from agents.human_like_generator import HumanLikeGenerator
from scheduler import NovelScheduler
from qa import NovelQASystem
from integrations import FeedbackProcessor
```

### 实现要点

- 通过 `check_environment` 等函数实现核心流程编排
- 基于 PyTorch 构建，保证技术栈成熟稳定
- 代码结构清晰，模块间低耦合，便于扩展和维护

---
## License

MIT — free to use, modify and distribute.
