"""
高级优化器 - 整合各种优化功能
"""

from typing import Dict, Any
from utils import LLMClient, get_logger
from .quality_analyzer import QualityAnalyzer
from .text_humanizer import TextHumanizer
from .style_optimizer import StyleOptimizer

logger = get_logger('advanced_optimizer')

class AdvancedOptimizer:
    """高级内容优化器"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.quality_analyzer = QualityAnalyzer()
        self.text_humanizer = TextHumanizer(self.llm)
        self.style_optimizer = StyleOptimizer(self.llm)
    
    def comprehensive_optimize(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """全面优化内容"""
        try:
            # 分析原始质量
            original_quality = self.quality_analyzer.analyze(content)
            
            # 人性化处理
            humanize_result = self.text_humanizer.humanize(content, aggressive=True)
            optimized_content = humanize_result.get('humanized_text', content)
            
            # 风格优化
            style_result = self.style_optimizer.optimize(optimized_content, {
                'vivid_description': True,
                'dialogue_variation': True,
                'rhythm_adjustment': True,
                'expression_personalization': True
            })
            final_content = style_result.get('optimized_text', optimized_content)
            
            # 分析优化后质量
            final_quality = self.quality_analyzer.analyze(final_content)
            
            quality_improvement = final_quality['overall_score'] - original_quality['overall_score']
            
            return {
                'optimization_success': quality_improvement > 0.1,
                'optimized_content': final_content,
                'quality_improvement': quality_improvement,
                'improvements': humanize_result.get('improvements', []) + style_result.get('applied_optimizations', [])
            }
            
        except Exception as e:
            logger.error(f"全面优化失败: {e}")
            return {
                'optimization_success': False,
                'optimized_content': content,
                'quality_improvement': 0,
                'improvements': []
            }
