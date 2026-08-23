"""基于Instructor的结构化输出 - 避免JSON解析错误"""
from typing import List, Optional
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI
import os
from utils import get_logger

logger = get_logger('structured_output')

# 定义小说大纲的数据模型
class Character(BaseModel):
    """角色模型"""
    name: str = Field(description="角色姓名")
    personality: str = Field(description="性格特征，用顿号分隔")
    appearance: str = Field(description="外貌描述")
    background: str = Field(description="背景故事")
    character_arc: str = Field(description="角色发展弧线")

class ChapterPlan(BaseModel):
    """章节规划模型"""
    chapter_number: int = Field(description="章节编号")
    chapter_title: str = Field(description="章节标题")
    plot_summary: str = Field(description="情节摘要")
    key_events: List[str] = Field(description="关键事件列表")
    word_count: int = Field(description="目标字数", ge=1000, le=10000)
    characters_involved: List[str] = Field(description="涉及的角色名称")

class NovelOutline(BaseModel):
    """小说大纲模型"""
    title: str = Field(description="小说标题")
    genre: str = Field(description="题材类型")
    theme: str = Field(description="主题思想")
    world_setting: str = Field(description="世界观设定")
    main_characters: List[Character] = Field(description="主要角色列表", min_items=1)
    chapter_plans: List[ChapterPlan] = Field(description="章节规划列表", min_items=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "修仙传奇",
                "genre": "玄幻修真",
                "theme": "逆天改命，追求大道",
                "world_setting": "修真世界，灵气复苏",
                "main_characters": [
                    {
                        "name": "林凡",
                        "personality": "坚韧、果敢、重情义",
                        "appearance": "剑眉星目，身材修长",
                        "background": "普通少年，意外获得传承",
                        "character_arc": "从凡人到修真强者"
                    }
                ],
                "chapter_plans": []
            }
        }

class StructuredOutputClient:
    """
    结构化输出客户端
    
    优势：
    - 使用Instructor + Pydantic强制类型
    - 自动验证和重试
    - 避免JSON解析错误
    - 类型安全
    """
    
    def __init__(self):
        # 从环境变量获取配置
        api_key = os.getenv("HEPAI_API_KEY")
        base_url = os.getenv("HEPAI_BASE_URL", "https://aiapi.ihep.ac.cn/apiv2")
        model = os.getenv("HEPAI_MODEL", "hepai/deepseek-r1:671b")
        
        # 创建OpenAI客户端
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # 使用Instructor包装，自动处理结构化输出
        self.client = instructor.from_openai(client)
        self.model = model
        
        logger.info("结构化输出客户端初始化完成")
    
    def generate_outline(self, genre: str = "", style: str = "", 
                        core_settings: str = "") -> NovelOutline:
        """
        生成小说大纲（结构化输出）
        
        Instructor会自动：
        - 强制LLM输出符合NovelOutline模型的JSON
        - 验证所有字段
        - 自动重试（如果输出不符合）
        - 类型转换
        
        Returns:
            NovelOutline对象（不是字符串，是类型安全的对象）
        """
        prompt = f"""
请创作一个小说大纲。

要求：
- 题材：{genre or '自由发挥'}
- 风格：{style or '自由发挥'}
- 核心设定：{core_settings or '自由发挥'}

请生成完整的小说大纲，包括：
1. 小说标题和主题
2. 世界观设定
3. 至少3个主要角色
4. 至少10章的章节规划
"""
        
        try:
            # Instructor自动处理结构化输出
            outline = self.client.chat.completions.create(
                model=self.model,
                response_model=NovelOutline,  # 指定返回模型
                messages=[
                    {"role": "system", "content": "你是一个专业的小说大纲规划师"},
                    {"role": "user", "content": prompt}
                ],
                max_retries=3  # 自动重试3次
            )
            
            logger.info(f"生成大纲成功: {outline.title}")
            return outline
            
        except Exception as e:
            logger.error(f"生成大纲失败: {e}")
            raise
    
    def generate_chapter_plan(self, chapter_number: int, 
                             previous_summary: str = "",
                             outline_context: str = "") -> ChapterPlan:
        """
        生成章节规划（结构化输出）
        
        Returns:
            ChapterPlan对象
        """
        prompt = f"""
请为第{chapter_number}章制定详细规划。

大纲背景：
{outline_context}

前文摘要：
{previous_summary}

请生成本章的详细规划。
"""
        
        try:
            plan = self.client.chat.completions.create(
                model=self.model,
                response_model=ChapterPlan,
                messages=[
                    {"role": "system", "content": "你是一个专业的章节规划师"},
                    {"role": "user", "content": prompt}
                ],
                max_retries=3
            )
            
            logger.info(f"生成章节规划成功: 第{chapter_number}章 - {plan.chapter_title}")
            return plan
            
        except Exception as e:
            logger.error(f"生成章节规划失败: {e}")
            raise
    
    def convert_to_dict(self, model_instance: BaseModel) -> dict:
        """将Pydantic模型转换为字典"""
        return model_instance.model_dump()
    
    def convert_to_json(self, model_instance: BaseModel) -> str:
        """将Pydantic模型转换为JSON字符串"""
        return model_instance.model_dump_json(indent=2, ensure_ascii=False)


# 使用示例
if __name__ == "__main__":
    # 创建客户端
    client = StructuredOutputClient()
    
    # 生成大纲 - 返回的是类型安全的对象，不是字符串！
    outline = client.generate_outline(
        genre="玄幻修真",
        style="热血爽文",
        core_settings="主角获得系统，逆天改命"
    )
    
    # 可以直接访问属性，有IDE自动补全
    print(f"标题: {outline.title}")
    print(f"主角: {outline.main_characters[0].name}")
    print(f"第一章: {outline.chapter_plans[0].chapter_title}")
    
    # 转换为字典或JSON
    outline_dict = client.convert_to_dict(outline)
    outline_json = client.convert_to_json(outline)

