"""基于LlamaIndex的世界观知识库 - 使用成熟框架，智能检索"""
import os
from typing import List, Dict, Optional
from llama_index.core import VectorStoreIndex, Document, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from utils import get_logger

logger = get_logger('lorebook_llamaindex')

class LorebookLlamaIndex:
    """
    基于LlamaIndex的世界观知识库
    
    优势：
    - 使用LlamaIndex的智能索引
    - 自动优化检索
    - 支持多种查询模式
    - 内置缓存和优化
    """
    
    def __init__(self, persist_dir: str = "data/lorebook_index"):
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        
        # 配置本地embedding模型
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # 配置节点解析器
        Settings.node_parser = SimpleNodeParser.from_defaults(
            chunk_size=512,
            chunk_overlap=50
        )
        
        # 加载或创建索引
        self.index = self._load_or_create_index()
        self.documents: Dict[str, Document] = {}
        
        logger.info(f"Lorebook初始化完成，索引目录: {persist_dir}")
    
    def _load_or_create_index(self):
        """加载已有索引或创建新索引"""
        try:
            # 尝试加载已有索引
            storage_context = StorageContext.from_defaults(
                persist_dir=self.persist_dir
            )
            index = load_index_from_storage(storage_context)
            logger.info("加载已有索引成功")
            return index
        except Exception as e:
            logger.info(f"创建新索引: {e}")
            # 创建新索引
            index = VectorStoreIndex([])
            return index
    
    def add_entry(self, title: str, category: str, content: str, 
                  triggers: List[str] = None, priority: int = 5) -> str:
        """
        添加词条
        
        LlamaIndex会自动：
        - 分块处理长文本
        - 向量化内容
        - 建立索引
        - 优化检索
        """
        entry_id = f"entry_{len(self.documents) + 1:03d}"
        
        # 构建文档内容
        doc_text = f"【{title}】（{category}）\n{content}"
        
        # 创建LlamaIndex Document
        doc = Document(
            text=doc_text,
            metadata={
                "entry_id": entry_id,
                "title": title,
                "category": category,
                "triggers": triggers or [],
                "priority": priority
            },
            id_=entry_id
        )
        
        # 添加到索引
        self.documents[entry_id] = doc
        self.index.insert(doc)
        
        # 持久化
        self._persist()
        
        logger.info(f"添加词条: {title} (ID: {entry_id})")
        return entry_id
    
    def query_relevant(self, text: str, top_k: int = 5) -> List[Dict]:
        """
        查询相关词条
        
        LlamaIndex会自动：
        - 理解查询意图
        - 检索最相关内容
        - 按相似度排序
        - 返回上下文
        """
        # 使用LlamaIndex的查询引擎
        query_engine = self.index.as_query_engine(
            similarity_top_k=top_k,
            response_mode="no_text"  # 只返回节点，不生成回答
        )
        
        # 执行查询
        response = query_engine.query(text)
        
        # 提取结果
        results = []
        for node in response.source_nodes:
            results.append({
                "content": node.node.text,
                "metadata": node.node.metadata,
                "score": node.score
            })
        
        return results
    
    def get_context_for_generation(self, current_text: str, max_entries: int = 3) -> str:
        """
        获取用于生成的上下文
        
        自动检索最相关的世界观设定
        """
        results = self.query_relevant(current_text, top_k=max_entries)
        
        if not results:
            return ""
        
        context = "【相关世界观设定】\n"
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            context += f"\n{i}. {metadata.get('title', '未命名')}\n"
            context += f"{result['content']}\n"
        
        return context
    
    def get_entries_by_category(self, category: str) -> List[Dict]:
        """根据类别获取词条"""
        results = []
        for entry_id, doc in self.documents.items():
            if doc.metadata.get('category') == category:
                results.append({
                    "id": entry_id,
                    "title": doc.metadata.get('title'),
                    "content": doc.text,
                    "metadata": doc.metadata
                })
        return results
    
    def update_entry(self, entry_id: str, updates: Dict):
        """更新词条"""
        if entry_id in self.documents:
            doc = self.documents[entry_id]
            
            # 更新metadata
            for key, value in updates.items():
                if key in doc.metadata:
                    doc.metadata[key] = value
            
            # 如果更新了内容，需要重建文档
            if 'content' in updates:
                title = doc.metadata.get('title', '')
                category = doc.metadata.get('category', '')
                doc.text = f"【{title}】（{category}）\n{updates['content']}"
            
            # 重新插入索引
            self.index.delete_ref_doc(entry_id)
            self.index.insert(doc)
            
            self._persist()
            logger.info(f"更新词条: {entry_id}")
    
    def delete_entry(self, entry_id: str):
        """删除词条"""
        if entry_id in self.documents:
            self.index.delete_ref_doc(entry_id)
            del self.documents[entry_id]
            self._persist()
            logger.info(f"删除词条: {entry_id}")
    
    def _persist(self):
        """持久化索引"""
        try:
            self.index.storage_context.persist(persist_dir=self.persist_dir)
        except Exception as e:
            logger.error(f"持久化索引失败: {e}")
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        categories = {}
        for doc in self.documents.values():
            cat = doc.metadata.get('category', '未分类')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_entries": len(self.documents),
            "categories": categories,
            "index_size": len(self.index.docstore.docs)
        }

