"""
人性化内容生成器
专门解决AI小说的"AI味"问题，让内容更加自然、有温度
"""

import json
from typing import Dict, List, Any, Optional
from utils import LLMClient, get_logger

logger = get_logger('human_like_generator')

class HumanLikeGenerator:
    """人性化内容生成器"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        
    def generate_human_like_chapter(self, chapter_plan: Dict[str, Any], 
                                  previous_context: Optional[Dict[str, Any]] = None,
                                  quality_mode: str = 'standard') -> Dict[str, Any]:
        """生成人性化章节"""
        try:
            # 基础内容生成
            content = self._generate_base_content(chapter_plan, previous_context)
            
            # 人性化优化
            humanized_content = self._humanize_content(content, quality_mode)
            
            # 质量评估
            quality_score = self._assess_quality(humanized_content)
            
            return {
                'final_content': humanized_content,
                'final_quality': {'overall_score': quality_score},
                'human_likeness_score': quality_score * 0.85  # 简化评分
            }
        
        except Exception as e:
            logger.error(f"人性化章节生成失败: {e}")
            return {
                'final_content': "生成失败",
                'final_quality': {'overall_score': 0},
                'human_likeness_score': 0
            }
    
    def _generate_base_content(self, chapter_plan: Dict[str, Any], 
                              previous_context: Optional[Dict[str, Any]]) -> str:
        """生成基础内容"""
        prompt = f"""
基于以下章节规划生成小说内容：

章节信息：
- 标题：{chapter_plan.get('chapter_title', '未知')}
- 主要情节：{chapter_plan.get('main_plot_points', [])}
- 角色发展：{chapter_plan.get('character_development', [])}

要求：
1. 字数2000-3000字
2. 情节紧凑有张力
3. 人物对话自然
4. 描写生动具体
"""
        
        return self.llm.generate(prompt, max_tokens=4000, temperature=0.8)
    
    def _humanize_content(self, content: str, quality_mode: str) -> str:
        """人性化内容"""
        if quality_mode == 'premium':
            return self._premium_humanize(content)
        else:
            return self._standard_humanize(content)
    
    def _standard_humanize(self, content: str) -> str:
        """标准人性化"""
        prompt = f"""
请优化以下小说内容，让它更有人情味：

原内容：
{content}

优化要求：
1. 语言更自然流畅
2. 对话更真实
3. 情感更有温度
4. 去除AI痕迹

请输出优化后的内容：
"""
        
        return self.llm.generate(prompt, max_tokens=4000, temperature=0.7)
    
    def _premium_humanize(self, content: str) -> str:
        """高级人性化"""
        prompt = f"""
作为资深小说编辑，请深度优化以下内容：

{content}

高级优化要求：
1. 语言表达更加生动有力
2. 人物对话个性化、真实化
3. 情感描写更有深度和共鸣
4. 叙事节奏更加合理
5. 细节描写更加精彩
6. 完全消除AI痕迹

请输出深度优化后的内容：
"""
        
        return self.llm.generate(prompt, max_tokens=4000, temperature=0.6)
    
    def _assess_quality(self, content: str) -> float:
        """评估内容质量"""
        # 简化质量评估
        word_count = len(content)
        if 2000 <= word_count <= 3500:
            return 8.5
        elif 1500 <= word_count <= 4000:
            return 7.5
        else:
            return 6.0
