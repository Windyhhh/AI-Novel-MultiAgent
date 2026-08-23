# 📚 AI 小说多智能体创作系统 | AI Novel Multi-Agent Writing System

> **基于多智能体协作的 AI 小说创作系统——大纲设计、角色构建、情节规划、章节写作、风格统一、质量审核，打造你的 AI 小说创作工坊。**
>
> *AI novel writing system based on multi-agent collaboration — outline design, character building, plot planning, chapter writing, style consistency, quality review, building your AI novel writing workshop.*

---

## ⭐ 核心卖点 | Why Star This

| 卖点 | Feature | 一句话 |
|------|---------|--------|
| 🤖 **多智能体协作** | Multi-Agent Collaboration | 作家、编辑、角色、评论家等多智能体协同创作 |
| 📖 **完整创作流程** | Full Writing Pipeline | 从灵感、大纲、角色到章节、审校的全流程自动化 |
| 🎭 **角色一致性** | Character Consistency | 角色记忆系统，保持人物性格和行为一致性 |
| ✍️ **风格可控** | Style Control | 支持多种文风，可模仿指定作家风格 |
| 🔍 **质量审核** | Quality Review | AI 编辑自动审核逻辑、节奏、文笔，给出修改建议 |

---

## 🏆 技术栈 | Tech Stack

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-green?logo=langchain)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal?logo=fastapi)
![Vue.js](https://img.shields.io/badge/Vue-3.0+-brightgreen?logo=vuedotjs)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7.0+-red?logo=redis)
![Vector DB](https://img.shields.io/badge/VectorDB-Chroma-orange?logo=chroma)
![Docker](https://img.shields.io/badge/Docker-24.0+-blue?logo=docker)

---

## 📊 智能体架构 | Agent Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        🎬 总控智能体 (Orchestrator)                   │
│              协调各智能体，管理创作流程，分配任务                      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
┌─────────▼─────────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐
│  📝 策划智能体      │ │  ✍️ 写作智能体      │ │  🔍 编辑智能体      │
│  (Planner Agent)   │ │  (Writer Agent)    │ │  (Editor Agent)    │
│                    │ │                    │ │                    │
│  - 灵感生成         │ │  - 章节写作         │ │  - 逻辑检查         │
│  - 大纲设计         │ │  - 对话生成         │ │  - 节奏把控         │
│  - 情节规划         │ │  - 场景描写         │ │  - 文笔润色         │
│  - 世界观构建       │ │  - 心理描写         │ │  - 风格统一         │
└─────────┬─────────┘ └─────────┬─────────┘ └─────────┬─────────┘
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
┌─────────▼─────────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐
│  🎭 角色智能体      │ │  📚 知识智能体      │ │  ⭐ 评论智能体      │
│  (Character Agent) │ │  (Knowledge Agent) │ │  (Critic Agent)    │
│                    │ │                    │ │                    │
│  - 角色设定         │ │  - 设定检索         │ │  - 质量评分         │
│  - 性格模拟         │ │  - 前文回顾         │ │  - 优缺点分析       │
│  - 对话风格         │ │  - 伏笔管理         │ │  - 改进建议         │
│  - 行为决策         │ │  - 一致性检查       │ │  - 读者视角         │
└───────────────────┘ └───────────────────┘ └───────────────────┘
```

---

## 🚀 快速开始 | Quick Start

```bash
git clone https://github.com/Windyhhh/AI-Novel-MultiAgent.git
cd AI-Novel-MultiAgent

# 1. 启动依赖服务
docker-compose up -d postgres redis chroma

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入大模型 API Key (支持 OpenAI / Qwen / 本地模型)

# 3. 安装后端依赖
cd backend
pip install -r requirements.txt

# 4. 初始化数据库
alembic upgrade head
python scripts/init_prompts.py

# 5. 启动后端
uvicorn app.main:app --reload --port 8000

# 6. 启动前端
cd ../frontend
npm install
npm run dev

# 7. 访问系统
# 创作平台: http://localhost:5173
# API 文档: http://localhost:8000/docs
```

---

## 📂 项目结构 | Project Structure

```
AI-Novel-MultiAgent/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py            # 应用入口
│   │   ├── config.py          # 配置
│   │   ├── api/               # API 路由
│   │   │   ├── novel.py       # 小说管理
│   │   │   ├── chapter.py     # 章节管理
│   │   │   ├── character.py   # 角色管理
│   │   │   ├── agent.py       # 智能体控制
│   │   │   └── writing.py     # 写作流程
│   │   ├── agents/            # 智能体
│   │   │   ├── base.py        # 智能体基类
│   │   │   ├── orchestrator.py # 总控智能体
│   │   │   ├── planner.py     # 策划智能体
│   │   │   ├── writer.py      # 写作智能体
│   │   │   ├── editor.py      # 编辑智能体
│   │   │   ├── character.py   # 角色智能体
│   │   │   ├── knowledge.py   # 知识智能体
│   │   │   └── critic.py      # 评论智能体
│   │   ├── models/            # 数据模型
│   │   │   ├── novel.py
│   │   │   ├── chapter.py
│   │   │   ├── character.py
│   │   │   └── agent.py
│   │   ├── services/          # 业务逻辑
│   │   │   ├── novel_service.py
│   │   │   ├── writing_service.py
│   │   │   ├── character_service.py
│   │   │   └── memory_service.py
│   │   ├── llm/               # 大模型封装
│   │   │   ├── base.py        # 基类
│   │   │   ├── openai.py      # OpenAI
│   │   │   ├── qwen.py        # 通义千问
│   │   │   ├── claude.py      # Claude
│   │   │   └── local.py       # 本地模型
│   │   ├── memory/            # 记忆系统
│   │   │   ├── character_memory.py # 角色记忆
│   │   │   ├── plot_memory.py  # 情节记忆
│   │   │   ├── style_memory.py # 风格记忆
│   │   │   └── vector_store.py # 向量存储
│   │   ├── prompts/           # Prompt 模板
│   │   │   ├── planner_prompts.py
│   │   │   ├── writer_prompts.py
│   │   │   ├── editor_prompts.py
│   │   │   ├── character_prompts.py
│   │   │   └── critic_prompts.py
│   │   └── utils/             # 工具函数
│   ├── scripts/               # 脚本
│   │   ├── init_prompts.py
│   │   └── import_novel.py
│   ├── alembic/               # 数据库迁移
│   └── requirements.txt
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── views/              # 页面
│   │   │   ├── Dashboard.vue   # 创作总览
│   │   │   ├── NovelList.vue   # 小说列表
│   │   │   ├── NovelEditor.vue # 小说编辑器
│   │   │   ├── ChapterWriter.vue # 章节写作
│   │   │   ├── CharacterStudio.vue # 角色工作室
│   │   │   ├── OutlineDesigner.vue # 大纲设计
│   │   │   └── Settings.vue    # 设置
│   │   ├── components/         # 组件
│   │   │   ├── editor/         # 编辑器组件
│   │   │   │   ├── RichTextEditor.vue
│   │   │   │   ├── ChapterOutline.vue
│   │   │   │   └── WritingAssistant.vue
│   │   │   ├── character/      # 角色组件
│   │   │   │   ├── CharacterCard.vue
│   │   │   │   ├── CharacterProfile.vue
│   │   │   │   └── RelationshipGraph.vue
│   │   │   ├── agent/          # 智能体组件
│   │   │   │   ├── AgentStatus.vue
│   │   │   │   ├── AgentChat.vue
│   │   │   │   └── WritingProgress.vue
│   │   │   └── common/
│   │   ├── api/                # API 调用
│   │   ├── store/              # Pinia
│   │   └── router/             # 路由
│   └── package.json
├── prompts/                    # Prompt 模板库
│   ├── styles/                 # 文风模板
│   │   ├── xianxia.md         # 仙侠风
│   │   ├── xuanhuan.md        # 玄幻风
│   │   ├── dushi.md           # 都市风
│   │   ├── lishi.md           # 历史风
│   │   └── kehuan.md          # 科幻风
│   ├── structures/             # 结构模板
│   │   ├── three_act.md       # 三幕式
│   │   ├── hero_journey.md    # 英雄之旅
│   │   └── save_the_cat.md    # 救猫咪
│   └── characters/             # 角色模板
│       ├── protagonist.md
│       ├── antagonist.md
│       └── mentor.md
├── examples/                   # 示例小说
│   ├── sample_novel.json
│   └── sample_characters.json
├── docker-compose.yml          # Docker 编排
├── .env.example                # 环境变量示例
└── README.md
```

---

## 🔬 核心智能体 | Core Agents

### 总控智能体 | Orchestrator Agent

```python
# agents/orchestrator.py - 总控智能体
from typing import Dict, List, Optional
from app.agents.base import BaseAgent
from app.agents.planner import PlannerAgent
from app.agents.writer import WriterAgent
from app.agents.editor import EditorAgent
from app.agents.character import CharacterAgent
from app.agents.knowledge import KnowledgeAgent
from app.agents.critic import CriticAgent

class OrchestratorAgent(BaseAgent):
    """总控智能体: 协调各智能体，管理创作流程"""
    
    def __init__(self, llm, memory):
        super().__init__(llm, memory, role="总控", name="Orchestrator")
        self.planner = PlannerAgent(llm, memory)
        self.writer = WriterAgent(llm, memory)
        self.editor = EditorAgent(llm, memory)
        self.character = CharacterAgent(llm, memory)
        self.knowledge = KnowledgeAgent(llm, memory)
        self.critic = CriticAgent(llm, memory)
    
    async def create_novel(self, idea: str, genre: str, style: str) -> Dict:
        """从零开始创作小说"""
        self.log("开始小说创作流程")
        
        # 1. 策划阶段: 生成大纲和设定
        self.log("阶段1: 策划 - 生成大纲和设定")
        plan_result = await self.planner.plan_novel(idea, genre, style)
        
        # 2. 角色阶段: 构建主要角色
        self.log("阶段2: 角色 - 构建主要角色")
        characters = await self.character.create_characters(
            plan_result['outline'], 
            plan_result['world_setting']
        )
        
        # 3. 细化大纲: 逐章规划
        self.log("阶段3: 细化 - 逐章规划")
        detailed_outline = await self.planner.create_chapter_outlines(
            plan_result['outline'],
            characters
        )
        
        return {
            'novel_id': self.generate_id(),
            'idea': idea,
            'genre': genre,
            'style': style,
            'outline': plan_result['outline'],
            'world_setting': plan_result['world_setting'],
            'characters': characters,
            'chapter_outlines': detailed_outline,
            'status': 'planned'
        }
    
    async def write_chapter(self, novel_id: str, chapter_index: int) -> Dict:
        """写作单个章节"""
        self.log(f"开始写作第 {chapter_index + 1} 章")
        
        # 1. 获取上下文
        context = await self.knowledge.get_writing_context(novel_id, chapter_index)
        
        # 2. 写作智能体生成初稿
        self.log("步骤1: 写作智能体生成初稿")
        draft = await self.writer.write_chapter(
            context['chapter_outline'],
            context['characters'],
            context['previous_chapters'],
            context['world_setting']
        )
        
        # 3. 角色智能体检核角色一致性
        self.log("步骤2: 角色智能体检核一致性")
        character_review = await self.character.review_consistency(
            draft,
            context['characters'],
            context['character_memory']
        )
        
        # 4. 编辑智能体润色
        self.log("步骤3: 编辑智能体润色")
        edited = await self.editor.edit_chapter(
            draft,
            character_review,
            context['style_guide']
        )
        
        # 5. 评论智能体评分
        self.log("步骤4: 评论智能体评分")
        critique = await self.critic.review_chapter(
            edited,
            context['chapter_outline']
        )
        
        # 6. 如果评分不达标，返回修改
        if critique['score'] < 7.0:
            self.log(f"评分 {critique['score']} 不达标，返回修改")
            revised = await self.editor.revise(
                edited,
                critique['suggestions']
            )
            edited = revised
            critique = await self.critic.review_chapter(edited, context['chapter_outline'])
        
        # 7. 更新记忆
        await self.memory.update_chapter_memory(novel_id, chapter_index, edited)
        
        return {
            'chapter_index': chapter_index,
            'content': edited,
            'word_count': len(edited),
            'character_review': character_review,
            'critique': critique,
            'status': 'completed'
        }
    
    async def batch_write(self, novel_id: str, 
                          start_chapter: int, 
                          end_chapter: int) -> List[Dict]:
        """批量写作多个章节"""
        results = []
        for i in range(start_chapter, end_chapter):
            result = await self.write_chapter(novel_id, i)
            results.append(result)
            self.log(f"第 {i+1} 章完成，字数: {result['word_count']}")
        return results
```

### 写作智能体 | Writer Agent

```python
# agents/writer.py - 写作智能体
from app.agents.base import BaseAgent
from app.prompts.writer_prompts import WRITER_PROMPTS

class WriterAgent(BaseAgent):
    """写作智能体: 负责章节内容创作"""
    
    def __init__(self, llm, memory):
        super().__init__(llm, memory, role="作家", name="Writer")
    
    async def write_chapter(self, outline: Dict, characters: List[Dict],
                            previous_chapters: List[str], 
                            world_setting: Dict) -> str:
        """写作章节"""
        
        # 1. 构建写作 Prompt
        prompt = self._build_writing_prompt(
            outline, characters, previous_chapters, world_setting
        )
        
        # 2. 分场景写作 (每章 3-5 个场景)
        scenes = outline.get('scenes', [])
        chapter_content = ""
        
        for i, scene in enumerate(scenes):
            self.log(f"写作场景 {i+1}/{len(scenes)}: {scene.get('title', '')}")
            
            scene_prompt = self._build_scene_prompt(
                scene, characters, chapter_content, world_setting
            )
            
            scene_content = await self.llm.generate(
                scene_prompt,
                temperature=0.8,
                max_tokens=2000
            )
            
            chapter_content += scene_content + "\n\n"
            
            # 实时更新上下文记忆
            await self.memory.add_scene_memory(scene_content)
        
        # 3. 章节过渡和收尾
        if outline.get('ending'):
            ending_prompt = WRITER_PROMPTS['chapter_ending'].format(
                chapter_content=chapter_content,
                ending_hint=outline['ending']
            )
            ending = await self.llm.generate(ending_prompt, temperature=0.7)
            chapter_content += ending
        
        return chapter_content.strip()
    
    def _build_writing_prompt(self, outline, characters, previous, world):
        """构建写作 Prompt"""
        character_desc = self._format_characters(characters)
        previous_summary = self._summarize_previous(previous)
        
        return WRITER_PROMPTS['chapter_writing'].format(
            chapter_title=outline.get('title', ''),
            chapter_summary=outline.get('summary', ''),
            key_events='\n'.join([f"- {e}" for e in outline.get('key_events', [])]),
            characters=character_desc,
            previous_summary=previous_summary,
            world_setting=world.get('description', ''),
            writing_style=world.get('style', '现实主义'),
            target_words=outline.get('target_words', 3000)
        )
    
    def _format_characters(self, characters):
        """格式化角色信息"""
        result = []
        for char in characters:
            result.append(f"""
【{char['name']}】
- 身份: {char.get('identity', '')}
- 性格: {char.get('personality', '')}
- 外貌: {char.get('appearance', '')}
- 说话风格: {char.get('speech_style', '')}
- 当前状态: {char.get('current_state', '')}
""")
        return '\n'.join(result)
```

### 角色智能体 | Character Agent

```python
# agents/character.py - 角色智能体
from app.agents.base import BaseAgent
from app.memory.character_memory import CharacterMemory
from app.prompts.character_prompts import CHARACTER_PROMPTS

class CharacterAgent(BaseAgent):
    """角色智能体: 负责角色构建和一致性维护"""
    
    def __init__(self, llm, memory):
        super().__init__(llm, memory, role="角色设计师", name="Character")
        self.character_memory = CharacterMemory(memory.vector_store)
    
    async def create_characters(self, outline: Dict, world_setting: Dict) -> List[Dict]:
        """根据大纲创建主要角色"""
        
        # 1. 分析大纲需要的角色
        analysis_prompt = CHARACTER_PROMPTS['analyze_needed_characters'].format(
            outline=outline,
            world_setting=world_setting
        )
        needed_chars = await self.llm.generate(analysis_prompt, temperature=0.7)
        
        # 2. 逐个创建角色
        characters = []
        for char_type in ['protagonist', 'antagonist', 'mentor', 'ally', 'rival']:
            char = await self._create_character(char_type, outline, world_setting)
            if char:
                characters.append(char)
                await self.character_memory.save_character(char)
        
        return characters
    
    async def _create_character(self, char_type: str, outline: Dict, 
                                 world_setting: Dict) -> Dict:
        """创建单个角色"""
        prompt = CHARACTER_PROMPTS[f'create_{char_type}'].format(
            outline=outline,
            world_setting=world_setting
        )
        
        char_data = await self.llm.generate(prompt, temperature=0.8)
        
        return {
            'id': self.generate_id(),
            'type': char_type,
            'name': char_data.get('name'),
            'identity': char_data.get('identity'),
            'age': char_data.get('age'),
            'gender': char_data.get('gender'),
            'appearance': char_data.get('appearance'),
            'personality': char_data.get('personality'),
            'background': char_data.get('background'),
            'motivation': char_data.get('motivation'),
            'speech_style': char_data.get('speech_style'),
            'abilities': char_data.get('abilities', []),
            'relationships': char_data.get('relationships', {}),
            'character_arc': char_data.get('character_arc'),
            'current_state': '初始状态'
        }
    
    async def review_consistency(self, chapter_content: str, 
                                  characters: List[Dict],
                                  character_memory: Dict) -> Dict:
        """审核章节中角色的一致性"""
        
        # 1. 提取章节中角色的言行
        extraction_prompt = CHARACTER_PROMPTS['extract_character_actions'].format(
            chapter_content=chapter_content,
            characters=[c['name'] for c in characters]
        )
        actions = await self.llm.generate(extraction_prompt, temperature=0.3)
        
        # 2. 对比角色设定
        issues = []
        for char_name, char_actions in actions.items():
            char = next((c for c in characters if c['name'] == char_name), None)
            if not char:
                continue
            
            # 检查性格一致性
            personality_issues = self._check_personality(
                char_actions, char['personality']
            )
            issues.extend(personality_issues)
            
            # 检查说话风格
            speech_issues = self._check_speech_style(
                char_actions.get('dialogues', []),
                char['speech_style']
            )
            issues.extend(speech_issues)
            
            # 检查能力边界
            ability_issues = self._check_abilities(
                char_actions.get('actions', []),
                char.get('abilities', [])
            )
            issues.extend(ability_issues)
        
        # 3. 更新角色记忆
        await self.character_memory.update_from_chapter(chapter_content)
        
        return {
            'consistent': len(issues) == 0,
            'issues': issues,
            'character_development': self._analyze_development(actions, characters),
            'suggestions': [f"修正: {issue}" for issue in issues[:5]]
        }
    
    def _check_personality(self, actions, personality):
        """检查性格一致性"""
        # 对比角色行为与性格设定
        # 例如: 内向角色不应该在公共场合大声演讲
        issues = []
        # ... 具体检查逻辑
        return issues
```

### 编辑智能体 | Editor Agent

```python
# agents/editor.py - 编辑智能体
from app.agents.base import BaseAgent
from app.prompts.editor_prompts import EDITOR_PROMPTS

class EditorAgent(BaseAgent):
    """编辑智能体: 负责内容润色和质量把控"""
    
    def __init__(self, llm, memory):
        super().__init__(llm, memory, role="编辑", name="Editor")
    
    async def edit_chapter(self, draft: str, character_review: Dict,
                           style_guide: Dict) -> str:
        """编辑润色章节"""
        
        edited = draft
        
        # 1. 逻辑检查
        self.log("检查逻辑连贯性")
        logic_issues = await self._check_logic(edited)
        if logic_issues:
            edited = await self._fix_logic(edited, logic_issues)
        
        # 2. 节奏调整
        self.log("调整叙事节奏")
        edited = await self._adjust_pacing(edited, style_guide)
        
        # 3. 文笔润色
        self.log("润色文笔")
        edited = await self._polish_prose(edited, style_guide)
        
        # 4. 角色问题修正
        if character_review and not character_review['consistent']:
            self.log("修正角色一致性问题")
            edited = await self._fix_character_issues(
                edited, character_review['issues']
            )
        
        # 5. 对话优化
        self.log("优化对话")
        edited = await self._optimize_dialogues(edited)
        
        # 6. 描写增强
        self.log("增强场景描写")
        edited = await self._enhance_description(edited)
        
        return edited
    
    async def _check_logic(self, content: str) -> List[Dict]:
        """检查逻辑问题"""
        prompt = EDITOR_PROMPTS['logic_check'].format(content=content)
        result = await self.llm.generate(prompt, temperature=0.2)
        return result.get('issues', [])
    
    async def _polish_prose(self, content: str, style: Dict) -> str:
        """文笔润色"""
        prompt = EDITOR_PROMPTS['prose_polish'].format(
            content=content,
            style=style.get('name', ''),
            tone=style.get('tone', ''),
            vocabulary_level=style.get('vocabulary', '中等')
        )
        return await self.llm.generate(prompt, temperature=0.6)
    
    async def _adjust_pacing(self, content: str, style: Dict) -> str:
        """调整叙事节奏"""
        # 分析当前节奏
        # 调整段落长度、场景切换、紧张度
        prompt = EDITOR_PROMPTS['pacing_adjust'].format(
            content=content,
            target_pacing=style.get('pacing', '中等')
        )
        return await self.llm.generate(prompt, temperature=0.5)
    
    async def revise(self, content: str, suggestions: List[str]) -> str:
        """根据建议修改"""
        prompt = EDITOR_PROMPTS['revise'].format(
            content=content,
            suggestions='\n'.join([f"- {s}" for s in suggestions])
        )
        return await self.llm.generate(prompt, temperature=0.7)
```

---

## 📊 创作流程 | Writing Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        第一阶段: 策划 (Planning)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. 灵感输入  →  2. 题材分析  →  3. 世界观构建                      │
│       │              │              │                                │
│       ▼              ▼              ▼                                │
│  4. 核心冲突  →  5. 故事大纲  →  6. 角色设定                        │
│       │              │              │                                │
│       ▼              ▼              ▼                                │
│  7. 逐章规划  →  8. 伏笔设计  →  9. 风格确定                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        第二阶段: 写作 (Writing)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  对每一章执行:                                                       │
│                                                                     │
│  1. 上下文获取 (前文回顾、角色状态、伏笔追踪)                         │
│           │                                                          │
│           ▼                                                          │
│  2. 场景分解 (3-5个场景，每场景有明确目标)                            │
│           │                                                          │
│           ▼                                                          │
│  3. 逐场景写作 (开头钩子→发展→高潮→过渡)                             │
│           │                                                          │
│           ▼                                                          │
│  4. 对话生成 (角色智能体确保对话符合人设)                              │
│           │                                                          │
│           ▼                                                          │
│  5. 描写增强 (环境、心理、动作描写)                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        第三阶段: 审校 (Review)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. 角色一致性检查 → 2. 逻辑连贯性检查 → 3. 叙事节奏检查             │
│           │                  │                  │                    │
│           ▼                  ▼                  ▼                    │
│  4. 文笔润色     → 5. 风格统一检查 → 6. 质量评分                     │
│           │                  │                  │                    │
│           └──────────────────┼──────────────────┘                    │
│                              ▼                                        │
│                    7. 评分 ≥ 7.0? ──Yes──→ 完成                      │
│                              │ No                                      │
│                              ▼                                        │
│                    8. 根据建议修改 → 返回步骤1                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 应用场景 | Use Cases

- 📖 **网文创作**：网络小说作者的AI写作助手
- 🎬 **剧本创作**：影视剧、短视频剧本创作
- 🎮 **游戏剧情**：游戏剧情和对话生成
- 📚 **内容创作**：自媒体故事、公众号文章创作
- 🎓 **写作教学**：创意写作课程教学辅助
- 🧪 **AI 研究**：多智能体协作、LLM 应用研究
- 💡 **灵感激发**：创作者的灵感来源和头脑风暴
- 🏢 **内容生产**：媒体机构的内容生产工具

---

## 📚 参考文献 | References

- Brown, T., et al. "Language Models are Few-Shot Learners." NeurIPS 2020.
- "The Anatomy of Story" by John Truby. 2007.
- "Save the Cat! Writes a Novel" by Jessica Brody. 2018.
- "Characters and Viewpoint" by Orson Scott Card. 1988.
- Park, J., et al. "Generative Agents: Interactive Simulacra of Human Behavior." UIST 2023.
- "Writing Fiction: A Guide to Narrative Craft" by Janet Burroway. 2010.

---

## 📄 License

MIT License — 自由使用、修改和分发。

---

> 💡 **多智能体协作的 AI 小说创作系统，Star ⭐ 开启你的 AI 写作之旅！**
