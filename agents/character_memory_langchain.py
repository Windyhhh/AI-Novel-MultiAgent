"""基于LangChain的角色记忆系统 - 使用成熟框架，稳定可靠"""
import os
from typing import Dict, List, Optional
from langchain.memory import VectorStoreRetrieverMemory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from utils import get_logger

logger = get_logger('character_memory_langchain')

class CharacterMemoryLangChain:
    """
    基于LangChain的角色记忆系统
    
    优势：
    - 使用LangChain的成熟Memory框架
    - 自动向量化和检索
    - 内置错误处理
    - 社区支持和文档完善
    """
    
    def __init__(self, character_name: str, persist_dir: str = "data/character_memory"):
        self.character_name = character_name
        self.persist_dir = os.path.join(persist_dir, character_name)
        os.makedirs(self.persist_dir, exist_ok=True)
        
        # 使用本地embedding模型（不需要API key）
        # 使用sentence-transformers，比OpenAI便宜且离线可用
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # 初始化向量存储
        self.vectorstore = Chroma(
            collection_name=f"char_{character_name}",
            embedding_function=self.embeddings,
            persist_directory=self.persist_dir
        )
        
        # 创建LangChain的Memory对象
        self.memory = VectorStoreRetrieverMemory(
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            memory_key="character_history",
            input_key="situation",
            output_key="behavior"
        )
        
        logger.info(f"角色记忆系统初始化完成: {character_name}")
    
    def add_behavior(self, chapter: int, action: str, emotion: str, context: str):
        """
        记录角色行为
        
        LangChain会自动：
        - 向量化内容
        - 存储到向量数据库
        - 建立索引
        """
        situation = f"第{chapter}章: {context}"
        behavior = f"{action} (情绪: {emotion})"
        
        # LangChain自动处理存储
        self.memory.save_context(
            inputs={"situation": situation},
            outputs={"behavior": behavior}
        )
        
        logger.debug(f"记录行为: {self.character_name} - 第{chapter}章")
    
    def get_relevant_behaviors(self, current_situation: str, k: int = 5) -> List[str]:
        """
        获取相关的历史行为
        
        LangChain会自动：
        - 向量化查询
        - 检索最相关的记忆
        - 按相似度排序
        """
        # 使用LangChain的load_memory_variables自动检索
        memory_vars = self.memory.load_memory_variables(
            {"situation": current_situation}
        )
        
        # 返回相关的历史行为
        history = memory_vars.get("character_history", "")
        return history.split("\n") if history else []
    
    def get_character_context(self, current_situation: str = "") -> str:
        """
        获取角色上下文（用于注入到生成提示词）
        
        LangChain自动检索最相关的记忆
        """
        if not current_situation:
            current_situation = "当前情境"
        
        memory_vars = self.memory.load_memory_variables(
            {"situation": current_situation}
        )
        
        context = f"【角色：{self.character_name}】\n"
        context += "最近相关行为：\n"
        context += memory_vars.get("character_history", "暂无历史记录")
        
        return context
    
    def search_behaviors(self, query: str, k: int = 3) -> List[Dict]:
        """
        搜索特定的行为记录
        
        使用LangChain的向量检索
        """
        # 直接使用vectorstore的相似度搜索
        docs = self.vectorstore.similarity_search(query, k=k)
        
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        return results
    
    def clear_memory(self):
        """清空记忆"""
        self.memory.clear()
        logger.info(f"清空角色记忆: {self.character_name}")
    
    @classmethod
    def from_character_data(cls, character_data: Dict, persist_dir: str = "data/character_memory"):
        """
        从角色数据创建记忆系统
        
        Args:
            character_data: 包含name, personality等的字典
        """
        name = character_data.get("name", "未命名角色")
        memory_system = cls(name, persist_dir)
        
        # 添加角色基础信息作为初始记忆
        personality = character_data.get("personality_traits", [])
        background = character_data.get("background", "")
        
        if personality or background:
            initial_context = f"角色设定: 性格={', '.join(personality)}, 背景={background}"
            memory_system.add_behavior(
                chapter=0,
                action="角色初始化",
                emotion="中性",
                context=initial_context
            )
        
        return memory_system


class CharacterMemoryManager:
    """管理多个角色的记忆系统"""
    
    def __init__(self, persist_dir: str = "data/character_memory"):
        self.persist_dir = persist_dir
        self.characters: Dict[str, CharacterMemoryLangChain] = {}
        logger.info("角色记忆管理器初始化完成")
    
    def get_or_create(self, character_name: str) -> CharacterMemoryLangChain:
        """获取或创建角色记忆系统"""
        if character_name not in self.characters:
            self.characters[character_name] = CharacterMemoryLangChain(
                character_name, self.persist_dir
            )
        return self.characters[character_name]
    
    def get_all_characters(self) -> List[str]:
        """获取所有角色名称"""
        return list(self.characters.keys())

