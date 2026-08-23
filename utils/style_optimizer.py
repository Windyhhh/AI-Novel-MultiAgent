"""
风格优化器
优化小说的写作风格，提升文学表现力
"""

import re
import json
from typing import Dict, List, Any
from utils import LLMClient, get_logger

logger = get_logger('style_optimizer')

class StyleOptimizer:
    """风格优化器"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def optimize(self, content: str, style_options: Dict[str, Any]) -> Dict[str, Any]:
        """风格优化"""
        try:
            optimized_text = content
            applied_optimizations = []
            
            # 生动描写优化
            if style_options.get('vivid_description', False):
                optimized_text = self._enhance_descriptions(optimized_text)
                applied_optimizations.append('生动描写优化')
            
            # 对话变化优化  
            if style_options.get('dialogue_variation', False):
                optimized_text = self._vary_dialogue(optimized_text)
                applied_optimizations.append('对话变化优化')
            
            # 节奏调整
            if style_options.get('rhythm_adjustment', False):
                optimized_text = self._adjust_pacing(optimized_text)
                applied_optimizations.append('节奏调整')
            
            # 表达个性化
            if style_options.get('expression_personalization', False):
                optimized_text = self._personalize_expressions(optimized_text)
                applied_optimizations.append('表达个性化')
            
            return {
                'success': True,
                'optimized_text': optimized_text,
                'applied_optimizations': applied_optimizations
            }
            
        except Exception as e:
            logger.error(f"风格优化失败: {e}")
            return {
                'success': False,
                'optimized_text': content,
                'error': str(e)
            }
    
    def _enhance_descriptions(self, text: str) -> str:
        """增强描写"""
        prompt = f"""
请优化以下文本的描写，让描写更加生动具体：

原文：
{text}

优化要求：
1. 环境描写更具体细腻
2. 人物描写更立体生动
3. 动作描写更精确有力
4. 情感描写更细腻真实
5. 避免空洞华丽的辞藻
6. 保持原文长度

请输出优化后的文本：
"""
        
        try:
            return self.llm.generate(prompt, max_tokens=4000, temperature=0.7)
        except Exception as e:
            logger.error(f"描写增强失败: {e}")
            return text
    
    def _vary_dialogue(self, text: str) -> str:
        """对话变化优化"""
        prompt = f"""
请优化以下文本的对话部分，让对话更加自然多样：

原文：
{text}

优化要求：
1. 每个角色对话有独特风格
2. 对话符合角色性格和身份
3. 语气词和口语化表达更丰富
4. 避免对话过于正式或程式化
5. 对话推动情节发展
6. 保持原文长度

请输出优化后的文本：
"""
        
        try:
            return self.llm.generate(prompt, max_tokens=4000, temperature=0.8)
        except Exception as e:
            logger.error(f"对话优化失败: {e}")
            return text
    
    def _adjust_pacing(self, text: str) -> str:
        """节奏调整"""
        prompt = f"""
请调整以下文本的叙事节奏：

原文：
{text}

调整要求：
1. 紧张场面节奏加快，句子简短有力
2. 抒情场面节奏放缓，句子舒展优美
3. 重要情节详细描述，次要情节简洁带过
4. 张弛有度，避免平铺直叙
5. 突出重点，主次分明
6. 保持原文长度

请输出调整后的文本：
"""
        
        try:
            return self.llm.generate(prompt, max_tokens=4000, temperature=0.6)
        except Exception as e:
            logger.error(f"节奏调整失败: {e}")
            return text
    
    def _personalize_expressions(self, text: str) -> str:
        """表达个性化"""
        prompt = f"""
请让以下文本的表达更加个性化：

原文：
{text}

个性化要求：
1. 用词更有特色，避免平庸表达
2. 句式更有变化，长短结合
3. 修辞手法运用恰当
4. 语言风格统一而有个性
5. 避免千篇一律的表达方式
6. 保持原文长度和内容

请输出个性化后的文本：
"""
        
        try:
            return self.llm.generate(prompt, max_tokens=4000, temperature=0.7)
        except Exception as e:
            logger.error(f"个性化表达失败: {e}")
            return text
