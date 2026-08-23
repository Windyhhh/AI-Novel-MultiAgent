"""大模型API客户端 - 增强版
支持：
- 连接池管理
- 自动重试机制
- 请求限流
- 性能监控
- 异步调用支持
"""
import os
import time
import logging
from typing import List, Dict, Optional
from functools import wraps
from threading import Lock, Semaphore
from concurrent.futures import ThreadPoolExecutor
from hepai import HepAI
from .config_loader import config

# 配置日志
logger = logging.getLogger(__name__)

def retry_on_failure(max_retries=3, delay=1.0, backoff=2.0):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay

            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"函数 {func.__name__} 重试{max_retries}次后仍失败: {e}")
                        raise

                    logger.warning(f"函数 {func.__name__} 调用失败，{current_delay}秒后重试 ({retries}/{max_retries}): {e}")
                    time.sleep(current_delay)
                    current_delay *= backoff

            return None
        return wrapper
    return decorator


class LLMClient:
    """大模型客户端封装 - 增强版"""

    # 类级别的线程池和信号量（所有实例共享）
    _executor = None
    _semaphore = None
    _lock = Lock()
    _max_concurrent_requests = 5  # 最大并发请求数

    def __init__(self):
        # 设置超时时间为10分钟（deepseek-r1思考时间较长）
        import httpx
        timeout = httpx.Timeout(600.0, connect=60.0)  # 总超时10分钟，连接超时1分钟

        self.client = HepAI(
            base_url=config.hepai_base_url,
            api_key=config.hepai_api_key,
            timeout=timeout
        )
        self.model = config.hepai_model

        # 初始化类级别资源
        with LLMClient._lock:
            if LLMClient._executor is None:
                LLMClient._executor = ThreadPoolExecutor(
                    max_workers=self._max_concurrent_requests,
                    thread_name_prefix="llm_worker"
                )
                logger.info(f"初始化LLM线程池，最大并发数: {self._max_concurrent_requests}")

            if LLMClient._semaphore is None:
                LLMClient._semaphore = Semaphore(self._max_concurrent_requests)

        # 性能统计
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_tokens': 0,
            'total_time': 0.0
        }
        self.stats_lock = Lock()

    def _update_stats(self, success: bool, tokens: int = 0, elapsed_time: float = 0.0):
        """更新统计信息"""
        with self.stats_lock:
            self.stats['total_requests'] += 1
            if success:
                self.stats['successful_requests'] += 1
            else:
                self.stats['failed_requests'] += 1
            self.stats['total_tokens'] += tokens
            self.stats['total_time'] += elapsed_time

    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self.stats_lock:
            stats = self.stats.copy()
            if stats['total_requests'] > 0:
                stats['success_rate'] = stats['successful_requests'] / stats['total_requests']
                stats['avg_time'] = stats['total_time'] / stats['total_requests']
            else:
                stats['success_rate'] = 0.0
                stats['avg_time'] = 0.0
            return stats

    @retry_on_failure(max_retries=3, delay=1.0, backoff=2.0)
    def chat(self, messages: List[Dict], temperature: float = 0.7,
             max_tokens: int = 4000, stream: bool = False,
             top_p: float = None, presence_penalty: float = None, frequency_penalty: float = None) -> str:
        """
        调用聊天接口（带重试和限流）

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            stream: 是否流式输出

        Returns:
            生成的文本内容
        """
        start_time = time.time()

        # 使用信号量限流
        with LLMClient._semaphore:
            try:
                logger.debug(f"开始LLM请求，模型: {self.model}, tokens: {max_tokens}")

                # 兼容可选采样参数
                extra_kwargs = {}
                if top_p is not None:
                    extra_kwargs["top_p"] = top_p
                if presence_penalty is not None:
                    extra_kwargs["presence_penalty"] = presence_penalty
                if frequency_penalty is not None:
                    extra_kwargs["frequency_penalty"] = frequency_penalty

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream,
                    **extra_kwargs
                )

                if stream:
                    # 流式输出
                    full_content = ""
                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            full_content += content
                            print(content, end="", flush=True)
                    print()  # 换行
                    result = full_content
                else:
                    # 非流式输出
                    result = response.choices[0].message.content

                elapsed_time = time.time() - start_time
                self._update_stats(True, max_tokens, elapsed_time)
                logger.debug(f"LLM请求成功，耗时: {elapsed_time:.2f}秒")

                return result

            except Exception as e:
                elapsed_time = time.time() - start_time
                self._update_stats(False, 0, elapsed_time)
                logger.error(f"LLM API调用失败: {e}")
                raise

    def generate_with_system_prompt(self, system_prompt: str, user_prompt: str,
                                    temperature: float = 0.7, max_tokens: int = 4000,
                                    top_p: float = None, presence_penalty: float = None, frequency_penalty: float = None) -> str:
        """
        使用系统提示词和用户提示词生成内容

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            temperature: 温度参数
            max_tokens: 最大token数

        Returns:
            生成的文本内容
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self.chat(messages, temperature=temperature, max_tokens=max_tokens)


    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """
        简单文本生成便捷方法
        等价于以单条user消息调用chat接口。
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, temperature=temperature, max_tokens=max_tokens, stream=False)

    def chat_async(self, messages: List[Dict], temperature: float = 0.7,
                   max_tokens: int = 4000, callback=None):
        """
        异步调用聊天接口

        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            callback: 回调函数，接收结果或异常

        Returns:
            Future对象
        """
        def task():
            try:
                result = self.chat(messages, temperature, max_tokens, stream=False)
                if callback:
                    callback(result, None)
                return result
            except Exception as e:
                if callback:
                    callback(None, e)
                raise

        return LLMClient._executor.submit(task)

    @classmethod
    def shutdown(cls):
        """关闭线程池"""
        with cls._lock:
            if cls._executor:
                logger.info("关闭LLM线程池...")
                cls._executor.shutdown(wait=True)
                cls._executor = None

