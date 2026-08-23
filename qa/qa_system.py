"""智能问答系统 - 基于RAG的小说内容问答（增强版）
支持：
- 查询结果缓存
- 批量索引优化
- 性能监控
"""
import os
import time
import hashlib
import logging
from typing import List, Dict, Optional
from functools import lru_cache
import chromadb
from chromadb.config import Settings
from utils import Storage, LLMClient, config, get_logger, perf_logger

# 配置日志
logger = get_logger('qa_system')

class NovelQASystem:
    """小说问答系统（增强版）"""

    def __init__(self, cache_size: int = 100):
        self.storage = Storage()
        self.llm = LLMClient()

        # 初始化向量数据库
        vector_db_dir = config.get('storage.vector_db_dir', 'data/vectordb')
        os.makedirs(vector_db_dir, exist_ok=True)

        # 配置ChromaDB设置（增加超时时间，支持国内网络）
        chroma_settings = Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )

        self.chroma_client = chromadb.PersistentClient(
            path=vector_db_dir,
            settings=chroma_settings
        )

        # 获取或创建集合（使用默认embedding函数，会自动下载模型）
        # 如果下载失败，可以手动下载模型到：
        # Windows: C:\Users\{用户名}\.cache\chroma\onnx_models\all-MiniLM-L6-v2\
        # Linux/Mac: ~/.cache/chroma/onnx_models/all-MiniLM-L6-v2/
        try:
            self.collection = self.chroma_client.get_or_create_collection(
                name="novel_content",
                metadata={"description": "小说章节内容"}
            )
            logger.info("ChromaDB集合初始化成功")
        except Exception as e:
            logger.error(f"ChromaDB初始化失败: {e}")
            logger.info("提示：如果是模型下载超时，可以：")
            logger.info("1. 使用代理或VPN")
            logger.info("2. 手动下载模型：https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz")
            logger.info("3. 解压到：C:\\Users\\{用户名}\\.cache\\chroma\\onnx_models\\all-MiniLM-L6-v2\\")
            raise

        # 查询缓存
        self.cache_size = cache_size
        self.query_cache = {}

        # 统计信息
        self.stats = {
            'total_queries': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }

        logger.info(f"QA系统初始化完成，缓存大小: {cache_size}")
    
    def _get_cache_key(self, question: str) -> str:
        """生成缓存键"""
        return hashlib.md5(question.encode('utf-8')).hexdigest()

    def _get_from_cache(self, question: str) -> Optional[str]:
        """从缓存获取答案"""
        cache_key = self._get_cache_key(question)
        if cache_key in self.query_cache:
            self.stats['cache_hits'] += 1
            logger.debug(f"缓存命中: {question[:50]}...")
            return self.query_cache[cache_key]
        self.stats['cache_misses'] += 1
        return None

    def _save_to_cache(self, question: str, answer: str):
        """保存到缓存"""
        cache_key = self._get_cache_key(question)

        # 如果缓存已满，删除最旧的条目
        if len(self.query_cache) >= self.cache_size:
            oldest_key = next(iter(self.query_cache))
            del self.query_cache[oldest_key]

        self.query_cache[cache_key] = answer
        logger.debug(f"保存到缓存: {question[:50]}...")

    def clear_cache(self):
        """清空缓存"""
        self.query_cache.clear()
        logger.info("查询缓存已清空")

    def index_all_chapters(self, batch_size: int = 100):
        """
        索引所有章节内容到向量数据库（批量优化）

        Args:
            batch_size: 批量处理大小
        """
        start_time = time.time()

        print("=" * 50)
        print("开始索引小说内容...")
        print("=" * 50)

        logger.info("开始索引所有章节")

        # 获取所有章节
        chapters = self.storage.get_all_content_text()

        if not chapters:
            logger.warning("没有找到任何章节内容")
            print("没有找到任何章节内容")
            return

        # 清空现有索引
        try:
            self.chroma_client.delete_collection("novel_content")
            self.collection = self.chroma_client.create_collection(
                name="novel_content",
                metadata={"description": "小说章节内容"}
            )
            logger.info("已清空现有索引")
        except Exception as e:
            logger.warning(f"清空索引时出错: {e}")

        # 准备批量数据
        all_documents = []
        all_metadatas = []
        all_ids = []

        for chapter in chapters:
            chapter_num = chapter['chapter_number']
            title = chapter['title']
            text = chapter['text']

            # 将长文本分段（每段约500字）
            segments = self._split_text(text, max_length=500)

            for i, segment in enumerate(segments):
                all_documents.append(segment)
                all_metadatas.append({
                    'chapter': chapter_num,
                    'title': title,
                    'segment': i
                })
                all_ids.append(f"chapter_{chapter_num}_seg_{i}")

        # 批量添加到向量数据库
        if all_documents:
            total_batches = (len(all_documents) + batch_size - 1) // batch_size
            logger.info(f"开始批量索引，共 {len(all_documents)} 个文本段，分 {total_batches} 批")

            for i in range(0, len(all_documents), batch_size):
                batch_docs = all_documents[i:i+batch_size]
                batch_metas = all_metadatas[i:i+batch_size]
                batch_ids = all_ids[i:i+batch_size]

                self.collection.add(
                    documents=batch_docs,
                    metadatas=batch_metas,
                    ids=batch_ids
                )

                batch_num = i // batch_size + 1
                logger.debug(f"完成第 {batch_num}/{total_batches} 批索引")

            elapsed_time = time.time() - start_time
            perf_logger.log_operation(
                'index_all_chapters',
                elapsed_time,
                success=True,
                chapters=len(chapters),
                segments=len(all_documents)
            )

            print(f"✓ 已索引 {len(chapters)} 章，共 {len(all_documents)} 个文本段")
            print(f"耗时: {elapsed_time:.2f}秒")
            logger.info(f"索引完成，耗时: {elapsed_time:.2f}秒")

            # 清空查询缓存
            self.clear_cache()
        else:
            logger.warning("没有内容需要索引")
            print("没有内容需要索引")
    
    def _split_text(self, text, max_length=500):
        """将长文本分段"""
        if len(text) <= max_length:
            return [text]
        
        segments = []
        current_segment = ""
        
        # 按句子分割
        sentences = text.replace('。', '。\n').replace('！', '！\n').replace('？', '？\n').split('\n')
        
        for sentence in sentences:
            if len(current_segment) + len(sentence) <= max_length:
                current_segment += sentence
            else:
                if current_segment:
                    segments.append(current_segment)
                current_segment = sentence
        
        if current_segment:
            segments.append(current_segment)
        
        return segments
    
    def query(self, question: str, top_k: int = 3, use_cache: bool = True) -> str:
        """
        查询问题（支持缓存）

        Args:
            question: 用户问题
            top_k: 返回最相关的top_k个结果
            use_cache: 是否使用缓存

        Returns:
            答案文本
        """
        start_time = time.time()

        self.stats['total_queries'] += 1

        print(f"\n问题: {question}")
        logger.info(f"收到查询: {question}")

        # 检查缓存
        if use_cache:
            cached_answer = self._get_from_cache(question)
            if cached_answer:
                elapsed_time = time.time() - start_time
                perf_logger.log_operation('query_cached', elapsed_time, success=True)
                logger.info(f"从缓存返回答案，耗时: {elapsed_time:.2f}秒")
                return cached_answer

        # 检查是否有索引内容
        count = self.collection.count()
        if count == 0:
            logger.warning("向量数据库为空")
            return "抱歉，还没有索引任何小说内容。请先生成章节内容。"

        try:
            # 检索相关内容
            logger.debug(f"开始向量检索，top_k={top_k}")
            results = self.collection.query(
                query_texts=[question],
                n_results=min(top_k, count)
            )

            if not results['documents'] or not results['documents'][0]:
                logger.warning("未找到相关内容")
                return "抱歉，没有找到相关内容。"

            # 构建上下文
            contexts = []
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                chapter = metadata['chapter']
                title = metadata['title']
                contexts.append(f"[第{chapter}章 {title}]\n{doc}")

            context_text = "\n\n".join(contexts)
            logger.debug(f"检索到 {len(contexts)} 个相关片段")

            # 构建提示词
            prompt = f"""基于以下小说内容回答问题。只使用提供的内容回答，不要编造信息。

小说内容：
{context_text}

问题：{question}

请根据上述小说内容回答问题。如果内容中没有相关信息，请明确说明。"""

            # 调用LLM生成答案
            logger.debug("调用LLM生成答案")
            answer = self.llm.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )

            # 保存到缓存
            if use_cache:
                self._save_to_cache(question, answer)

            elapsed_time = time.time() - start_time
            perf_logger.log_operation('query', elapsed_time, success=True, top_k=top_k)
            logger.info(f"查询完成，耗时: {elapsed_time:.2f}秒")

            return answer

        except Exception as e:
            elapsed_time = time.time() - start_time
            perf_logger.log_operation('query', elapsed_time, success=False)
            logger.error(f"查询失败: {e}", exc_info=True)
            return f"查询过程中出现错误: {str(e)}"
    
    def get_chapter_summary(self, chapter_number):
        """获取章节摘要"""
        chapter = self.storage.load_chapter(chapter_number)
        if not chapter:
            return f"未找到第{chapter_number}章"
        
        content = chapter.get('content', '')
        if len(content) > 200:
            summary = content[:200] + "..."
        else:
            summary = content
        
        return f"第{chapter_number}章 {chapter.get('title', '')}\n\n{summary}"
    
    def search_chapters(self, keyword: str) -> List[Dict]:
        """搜索包含关键词的章节"""
        start_time = time.time()

        logger.info(f"搜索关键词: {keyword}")
        chapters = self.storage.get_all_chapters()
        results = []

        for chapter in chapters:
            content = chapter.get('content', '')
            title = chapter.get('title', '')
            chapter_num = chapter.get('chapter_number', 0)

            if keyword in content or keyword in title:
                # 提取关键词上下文
                if keyword in content:
                    idx = content.index(keyword)
                    start = max(0, idx - 50)
                    end = min(len(content), idx + 50)
                    context = "..." + content[start:end] + "..."
                else:
                    context = title

                results.append({
                    'chapter': chapter_num,
                    'title': title,
                    'context': context
                })

        elapsed_time = time.time() - start_time
        perf_logger.log_operation('search_chapters', elapsed_time, success=True, results=len(results))
        logger.info(f"搜索完成，找到 {len(results)} 个结果，耗时: {elapsed_time:.2f}秒")

        return results

    def get_stats(self) -> Dict:
        """获取统计信息"""
        stats = self.stats.copy()
        if stats['total_queries'] > 0:
            stats['cache_hit_rate'] = stats['cache_hits'] / stats['total_queries']
        else:
            stats['cache_hit_rate'] = 0.0
        stats['cache_size'] = len(self.query_cache)
        stats['indexed_segments'] = self.collection.count()
        return stats

