"""
层次化小说生成器 - 参考Long-Novel-GPT的设计
实现大纲→章节→正文的三层生成架构
"""
from typing import Dict, List, Optional
from utils.context_manager import ContextManager
from utils.memory_system import ThreeLayerMemorySystem
from agents.smart_chapter_planner import SmartChapterPlanner
from prompts.chinese_novel_templates import get_template, CHAPTER_START_TEMPLATE
from utils import get_logger

logger = get_logger('hierarchical_generator')

class HierarchicalNovelGenerator:
    """
    层次化小说生成器
    
    三层架构（参考Long-Novel-GPT）：
    1. 大纲层（Outline Layer）- 整体故事框架
    2. 章节层（Chapter Layer）- 章节详细规划
    3. 正文层（Content Layer）- 具体内容生成
    
    集成组件：
    - ContextManager: 智能上下文管理
    - ThreeLayerMemorySystem: NovelAI风格记忆系统
    - SmartChapterPlanner: 智能章节规划
    - ChineseNovelTemplates: 中文小说Prompt模板
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.context_manager = ContextManager()
        self.memory_system = ThreeLayerMemorySystem()
        self.chapter_planner = SmartChapterPlanner()
        
        # 生成状态
        self.current_outline: Optional[Dict] = None
        self.chapter_plans: List[Dict] = []
        self.generated_chapters: List[Dict] = []
        
        logger.info("层次化生成器初始化完成")
    
    def generate_novel(self, theme: str, genre: str, style: str = "",
                      target_chapters: int = 50) -> Dict:
        """
        完整的小说生成流程
        
        Args:
            theme: 主题
            genre: 题材
            style: 风格
            target_chapters: 目标章节数
        
        Returns:
            生成的小说数据
        """
        logger.info(f"开始生成{genre}小说：{theme}")
        
        # 第一层：生成大纲
        self.current_outline = self.generate_outline(theme, genre, style)
        
        # 第二层：规划章节
        self.chapter_plans = self.chapter_planner.plan_chapters(
            self.current_outline, target_chapters
        )
        
        # 第三层：逐章生成内容
        self.generated_chapters = []
        for i, plan in enumerate(self.chapter_plans):
            chapter_content = self.generate_chapter_content(plan, i + 1)
            self.generated_chapters.append(chapter_content)
            
            # 更新上下文管理器
            self.context_manager.add_chapter(
                chapter_num=i + 1,
                content=chapter_content["content"],
                summary=chapter_content.get("summary", "")
            )
        
        novel_data = {
            "outline": self.current_outline,
            "chapter_plans": self.chapter_plans,
            "chapters": self.generated_chapters,
            "statistics": self._get_statistics()
        }
        
        logger.info(f"小说生成完成，共{len(self.generated_chapters)}章")
        return novel_data
    
    def generate_outline(self, theme: str, genre: str, style: str = "") -> Dict:
        """
        第一层：生成大纲
        
        使用结构化输出确保格式正确
        """
        from utils.structured_output import StructuredOutputClient
        
        client = StructuredOutputClient()
        outline = client.generate_outline(
            genre=genre,
            style=style,
            core_settings=theme
        )
        
        # 转换为字典格式
        outline_dict = client.convert_to_dict(outline)
        
        # 添加到Memory系统
        self.memory_system.add_lorebook_entry(
            entry_id="main_outline",
            title="主要大纲",
            content=f"主题：{theme}\n题材：{genre}\n风格：{style}",
            triggers=["大纲", "主题", "设定"],
            category="outline",
            priority=10
        )
        
        logger.info(f"大纲生成完成：{outline_dict.get('title', '未命名')}")
        return outline_dict
    
    def generate_chapter_content(self, chapter_plan: Dict, chapter_num: int) -> Dict:
        """
        第三层：生成章节内容
        
        Args:
            chapter_plan: 章节规划
            chapter_num: 章节编号
        
        Returns:
            章节内容字典
        """
        # 构建生成上下文
        context = self._build_generation_context(chapter_plan, chapter_num)
        
        # 选择合适的模板
        genre = self.current_outline.get("genre", "通用")
        template = get_template(genre)
        
        # 填充模板参数
        prompt = self._fill_template(template, chapter_plan, context)
        
        # 使用Memory系统构建完整prompt
        full_prompt = self.memory_system.build_prompt(prompt)
        
        # 调用LLM生成
        response = self._call_llm(full_prompt)
        
        # 处理生成结果
        chapter_content = {
            "chapter_number": chapter_num,
            "title": chapter_plan.get("chapter_title", f"第{chapter_num}章"),
            "content": response,
            "word_count": len(response),
            "summary": self._generate_chapter_summary(response),
            "plan": chapter_plan
        }
        
        logger.info(f"第{chapter_num}章生成完成，字数：{len(response)}")
        return chapter_content
    
    def _build_generation_context(self, chapter_plan: Dict, chapter_num: int) -> str:
        """
        构建生成上下文
        
        整合：
        - 大纲信息
        - 前文回顾
        - 角色状态
        - 章节规划
        """
        context_parts = []
        
        # 大纲信息
        if self.current_outline:
            context_parts.append(f"【小说标题】{self.current_outline.get('title', '')}")
            context_parts.append(f"【主题】{self.current_outline.get('theme', '')}")
            context_parts.append(f"【世界观】{self.current_outline.get('world_setting', '')}")
        
        # 前文回顾（使用ContextManager）
        if chapter_num > 1:
            previous_context = self.context_manager.build_context(
                current_chapter=chapter_num,
                include_recent=2
            )
            context_parts.append(previous_context)
        
        # 本章规划
        context_parts.append(f"\n【本章规划】")
        context_parts.append(f"章节类型：{chapter_plan.get('chapter_type', '')}")
        context_parts.append(f"节奏：{chapter_plan.get('pacing', '')}")
        context_parts.append(f"重点：{chapter_plan.get('focus', '')}")
        context_parts.append(f"氛围：{chapter_plan.get('atmosphere', '')}")
        
        if chapter_plan.get('plot_points'):
            context_parts.append(f"情节点：{', '.join(chapter_plan['plot_points'])}")
        
        return "\n".join(context_parts)
    
    def _fill_template(self, template: str, chapter_plan: Dict, context: str) -> str:
        """
        填充模板参数
        
        将章节规划和上下文信息填入模板
        """
        # 准备模板参数
        template_params = {
            "chapter_num": chapter_plan.get("chapter_number", 1),
            "word_count": chapter_plan.get("word_count", 3000),
            "pacing": chapter_plan.get("pacing", "正常"),
            "atmosphere": chapter_plan.get("atmosphere", "中性"),
            "current_plot": context,
            "protagonist": "主角",  # 可以从大纲中提取
            "world_setting": self.current_outline.get("world_setting", "") if self.current_outline else "",
        }
        
        # 安全地填充模板（避免KeyError）
        try:
            return template.format(**template_params)
        except KeyError as e:
            logger.warning(f"模板参数缺失：{e}，使用默认值")
            # 使用默认模板
            from prompts.chinese_novel_templates import GENERAL_TEMPLATE
            return GENERAL_TEMPLATE.format(**template_params)
    
    def _call_llm(self, prompt: str) -> str:
        """
        调用LLM生成内容
        
        TODO: 根据实际的LLM接口调整
        """
        try:
            # 这里需要根据实际的LLM客户端调整
            response = self.llm.generate(prompt)
            return response
        except Exception as e:
            logger.error(f"LLM调用失败：{e}")
            return f"[生成失败：{e}]"
    
    def _generate_chapter_summary(self, content: str, max_length: int = 150) -> str:
        """
        生成章节摘要
        
        简单实现：取前N个字符
        TODO: 可以用LLM生成更好的摘要
        """
        summary = content[:max_length]
        if len(content) > max_length:
            summary += "..."
        return summary
    
    def _get_statistics(self) -> Dict:
        """获取生成统计信息"""
        total_words = sum(ch.get("word_count", 0) for ch in self.generated_chapters)
        
        return {
            "total_chapters": len(self.generated_chapters),
            "total_words": total_words,
            "average_words_per_chapter": total_words // len(self.generated_chapters) if self.generated_chapters else 0,
            "context_stats": self.context_manager.get_statistics(),
            "memory_stats": self.memory_system.get_statistics()
        }
    
    # ==================== 实用方法 ====================
    
    def set_authors_note(self, note: str):
        """设置作者笔记（影响生成风格）"""
        self.memory_system.set_authors_note(note)
        logger.info(f"设置作者笔记：{note}")
    
    def add_lorebook_entry(self, title: str, content: str, triggers: List[str]):
        """添加世界观设定"""
        self.memory_system.add_lorebook_entry(
            entry_id=f"custom_{len(self.memory_system.lorebook)}",
            title=title,
            content=content,
            triggers=triggers,
            category="custom"
        )
    
    def regenerate_chapter(self, chapter_num: int) -> Dict:
        """重新生成指定章节"""
        if chapter_num <= len(self.chapter_plans):
            plan = self.chapter_plans[chapter_num - 1]
            new_content = self.generate_chapter_content(plan, chapter_num)
            
            # 更新已生成的章节
            if chapter_num <= len(self.generated_chapters):
                self.generated_chapters[chapter_num - 1] = new_content
            
            return new_content
        else:
            raise ValueError(f"章节编号超出范围：{chapter_num}")
