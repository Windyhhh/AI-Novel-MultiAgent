# 📚 AI小说多智能体创作系统 | AI Novel Multi-Agent Creation System

> **AI Novel Multi-Agent Creation System**
>
> 基于多智能体协作的 AI 小说创作平台，融合大纲生成、章节规划、内容创作、角色记忆、情节追踪等 16 个专业智能体，通过人性化后处理去除 AI 味，实现"像人写的"小说创作。支持 Web 界面、定时调度、飞书集成。
>
> An AI novel creation platform with 16 specialized agents (outline, chapter planning, content generation, character memory, plot tracking). Humanized post-processing removes AI flavor for "human-like" writing. Supports Web UI, scheduling, and Feishu integration.

---

## ✨ 核心亮点

| 维度 | 详情 |
|------|------|
| 🤖 多智能体 | **16 个**专业智能体协作创作 |
| 🧠 角色记忆 | 持久化角色设定与行为一致性 |
| 📝 去 AI 味 | 人性化后处理，目标 AI 感 ≤ 20% |
| 🎯 采样策略 | 4 套预设（默认/动作/对话/描写），参考 Kobold/NovelAI |
| 🌐 Web 界面 | Flask 全功能创作管理后台 |
| ⏰ 定时调度 | 每日自动生成章节，可配置时间和数量 |
| 💬 智能问答 | 基于已有内容的 QA 检索系统 |
| 📤 飞书集成 | 自动同步到飞书文档 |

---

## 🏗️ 多智能体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Orchestrator                         │
│              （智能体编排器，调度全流程）                      │
└──────────────┬──────────────────────────────────────────────┘
               │
    ┌──────────┼──────────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│大纲智能体│ │章节规划│ │内容生成│ │角色记忆│ │情节追踪│
│Outline │ │Chapter │ │Content │ │Character│ │Plot   │
│Agent   │ │Planning│ │Gen     │ │Memory  │ │Tracker│
└────────┘ └────────┘ └───┬────┘ └────────┘ └────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │分层生成器  │ │人性化生成 │ │悬疑专项   │
        │Hierarch- │ │Human-like│ │Mystery   │
        │ical      │ │Generator │ │Agent     │
        └──────────┘ └──────────┘ └──────────┘
```

### 智能体清单

| 智能体 | 文件 | 职责 |
|--------|------|------|
| 🎼 编排器 | `agent_orchestrator.py` | 全流程调度，智能体协作管理 |
| 🏭 工厂 | `agent_factory.py` | 智能体实例化与配置 |
| 📋 大纲 | `outline_agent.py` | 小说大纲生成与优化 |
| 📖 章节规划 | `chapter_planning_agent.py` | 单章内容规划与节奏控制 |
| ✍️ 内容生成 | `content_generation_agent.py` | 正文内容生成 |
| 🎭 角色记忆 | `character_memory_agent.py` | 角色设定持久化，行为一致性 |
| 🧩 情节追踪 | `plot_tracker_agent.py` | 伏笔追踪，情节连贯性 |
| 🏔️ 分层生成 | `hierarchical_generator.py` | 从大纲到段落的分层生成 |
| 🧑 人性化 | `human_like_generator.py` | 去 AI 味，句长变异，词汇多样性 |
| 🔍 悬疑专项 | `mystery_agent.py` | 悬疑类小说专项优化 |
| 🍅 番茄专项 | `tomato_novel_agent.py` | 番茄小说风格适配 |
| ⚡ 集成优化 | `integrated_optimization_pipeline.py` | 全链路质量优化 |

---

## 🎨 人性化后处理（去 AI 味）

系统内置多轮迭代的人性化后处理管线，目标：

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 总体质量分 | ≥ 85.0 | 综合质量评分 |
| 人类感分 | ≥ 80.0 | 拟人化程度 |
| AI 感上限 | ≤ 20.0 | 越低越好 |
| 句长变异系数 | ≥ 0.5 | burstiness，避免句式单调 |
| 词汇多样性 (TTR) | ≥ 0.6 | lexical diversity，避免重复用词 |

### 处理模式

| 模式 | 迭代轮数 | 适用场景 |
|------|---------|---------|
| `standard` | 1 轮 | 快速生成，日常更新 |
| `high` | 2 轮 | 质量优先，推荐默认 |
| `premium` | 3 轮 | 极致质量，关键章节 |

---

## 🎯 采样策略预设

参考 Kobold / NovelAI 的专业采样配置，内置 4 套预设：

| 预设 | Temperature | Top P | Presence Penalty | Frequency Penalty | 适用场景 |
|------|------------|-------|-----------------|------------------|---------|
| **default** | 0.8 | 0.9 | 0.3 | 0.2 | 通用创作 |
| **action** | 0.9 | 0.85 | 0.4 | 0.4 | 动作场景，节奏快 |
| **dialogue** | 0.7 | 0.9 | 0.2 | 0.3 | 对话场景，更稳定 |
| **description** | 0.8 | 0.95 | 0.1 | 0.1 | 环境描写，更发散 |

---

## 🚀 快速开始

### 环境要求

```bash
Python >= 3.8
Flask >= 2.0
requests >= 2.25
PyYAML >= 5.4
python-dotenv >= 0.19
```

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/Windyhhh/AI-Novel-MultiAgent.git
cd AI-Novel-MultiAgent

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 API
cp .env.example .env
# 编辑 .env，填入你的 API Key
```

### 配置 API

编辑 `.env` 文件：

```env
# HepAI API 配置
HEPAI_API_KEY=your_api_key_here
HEPAI_BASE_URL=https://aiapi.ihep.ac.cn/apiv2
HEPAI_MODEL=hepai/deepseek-r1:671b

# 系统配置
DAILY_SCHEDULE_TIME=09:00
CHAPTERS_PER_DAY=2
DEFAULT_CHAPTER_LENGTH=3000
```

### 启动 Web 界面

```bash
python main.py --mode web
```

访问 `http://localhost:5000` 即可使用全功能创作界面。

### 命令行模式

```bash
# 检查系统状态
python main.py --check

# 创建新小说
python main.py --mode create --genre "悬疑" --style "本格推理"

# 生成新章节
python main.py --mode generate --chapter 1

# 启动定时调度
python main.py --mode schedule
```

---

## 📁 项目结构

```
AI-Novel-MultiAgent/
├── README.md                          # 本文件
├── requirements.txt                   # Python 依赖
├── .gitignore                         # Git 忽略规则
├── .env.example                       # 环境变量模板
├── config.yaml                        # 系统配置文件
├── main.py                            # 主程序入口（CLI + Web）
├── app.py                             # Web 应用入口
├── agents/                            # 多智能体模块
│   ├── __init__.py
│   ├── agent_factory.py               # 智能体工厂
│   ├── agent_orchestrator.py          # 智能体编排器
│   ├── outline_agent.py               # 大纲生成智能体
│   ├── chapter_planning_agent.py      # 章节规划智能体
│   ├── content_generation_agent.py    # 内容生成智能体
│   ├── character_memory_agent.py      # 角色记忆智能体
│   ├── plot_tracker_agent.py          # 情节追踪智能体
│   ├── hierarchical_generator.py      # 分层生成器
│   ├── human_like_generator.py        # 人性化生成器
│   ├── mystery_agent.py               # 悬疑专项智能体
│   ├── tomato_novel_agent.py          # 番茄小说专项
│   ├── integrated_optimization_pipeline.py  # 集成优化管线
│   └── prompts.py                     # 智能体提示词
├── prompts/                           # 提示词模板
├── scheduler/                         # 定时调度模块
├── qa/                                # 智能问答模块
├── utils/                             # 工具函数
├── web/                               # Web 界面
│   ├── app.py                         # Flask 应用
│   └── templates/                     # HTML 模板
├── integrations/                      # 第三方集成
│   └── feishu.py                      # 飞书文档集成
├── examples/                          # 示例配置与输出
├── docs/                              # 文档
└── data/                              # 数据存储（运行时生成）
    ├── novels/                        # 小说项目
    ├── chapters/                      # 章节内容
    ├── outline.json                   # 大纲数据
    └── vectordb/                      # 向量数据库
```

---

## ⚙️ 配置说明

### 系统配置 (`config.yaml`)

```yaml
# 调度配置
scheduler:
  enabled: true
  schedule_time: "09:00"       # 每日生成时间
  chapters_per_day: 2           # 每日生成章节数

# 章节配置
chapter:
  default_length: 3000          # 默认章节字数
  min_length: 2000
  max_length: 5000

# 人性化处理
humanize:
  enabled: true
  mode: "high"                  # standard / high / premium
  max_iterations: 2

# Web 服务
web:
  host: "0.0.0.0"
  port: 5000
  debug: false
```

---

## 🎯 核心功能

### 1. 大纲生成
- 自主构思模式：AI 独立完成世界观、人物、情节线设计
- 协作模式：结合用户创意，AI 辅助完善
- 多轮迭代优化：大纲可反复修改完善

### 2. 章节创作
- 轻量 DOC 段落提纲：每章 6-8 个段落规划
- 分层生成：大纲 → 段落提纲 → 正文内容
- 实时进度显示：生成过程可监控

### 3. 角色一致性
- 持久化角色记忆库
- 自动检查角色行为一致性
- 角色关系图谱维护

### 4. 情节追踪
- 伏笔自动记录与回收提醒
- 时间线一致性检查
- 情节漏洞自动检测

### 5. 智能问答
- 基于已有内容的语义检索
- 支持角色名、地名、情节关键词查询
- 自动关联上下文章节

### 6. 定时调度
- 每日定时自动生成
- 可配置生成时间和章节数量
- 自动备份与版本管理

---

## 🔌 第三方集成

### 飞书文档
自动将生成的章节同步到飞书文档，支持多人协作编辑。

配置 `.env`：
```env
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_DOC_TOKEN=your_doc_token
```

---

## 📊 质量监控

系统内置多维度质量评估：

| 维度 | 指标 | 说明 |
|------|------|------|
| 流畅度 | 句长变异系数 | 避免句式单调 |
| 多样性 | TTR 词汇多样性 | 避免用词重复 |
| 一致性 | 角色行为匹配度 | 角色不 OOC |
| 连贯性 | 情节衔接评分 | 章节间过渡自然 |
| 原创性 | AI 感检测 | 越低越好 |

---

## 🎯 适用场景

- ✅ **网络小说创作** — 日更万字，稳定输出
- ✅ **剧本大纲设计** — 影视剧、游戏剧本
- ✅ **同人创作** — 基于已有 IP 的二次创作
- ✅ **写作辅助** — 人类作者的 AI 协作工具
- ✅ **内容生产** — 自媒体、公众号批量内容

---

## ⚠️ 注意事项

- API Key 请妥善保管，不要提交到公开仓库
- 生成内容需遵守平台规范和法律法规
- 建议定期备份 `data/` 目录
- 大模型生成内容可能存在幻觉，重要情节建议人工审核

---

## 📄 许可证

MIT License — 可自由使用、修改和分发。

---

## 🤝 引用

```bibtex
@misc{novel-multi-agent2025,
  title={AI Novel Multi-Agent Creation System},
  author={Windyhhh},
  year={2025},
  howpublished={\url{https://github.com/Windyhhh/AI-Novel-MultiAgent}}
}
```

---

<div align="center">

**📚 让 AI 成为你的创作搭档，写出有灵魂的故事 📚**

[报告问题](https://github.com/Windyhhh/AI-Novel-MultiAgent/issues) · [提出建议](https://github.com/Windyhhh/AI-Novel-MultiAgent/issues)

</div>
