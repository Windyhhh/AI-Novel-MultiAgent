"""
Self-Reflection Engine - 自我反思引擎
基于Self-RAG技术，为AI小说生成提供自我反思和质量评估能力
"""

import json
import re
from typing import Dict, List, Any, Tuple, Optional
from utils.llm_client import LLMClient
from utils.logger import get_logger

logger = get_logger(__name__)


class SelfReflectionEngine:
    """自我反思引擎，提供内容生成的自我评估和改进能力"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.reflection_tokens = {
            'retrieval': '[Retrieval]',
            'no_retrieval': '[No Retrieval]', 
            'relevant': '[Relevant]',
            'irrelevant': '[Irrelevant]',
            'fully_supported': '[Fully supported]',
            'partially_supported': '[Partially supported]',
            'no_support': '[No support]',
            'utility': '[Utility:{}]'  # 1-5 rating
        }
    
    def generate_with_reflection(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        带自我反思的内容生成
        
        Args:
            prompt: 生成提示
            context: 上下文信息
            
        Returns:
            包含生成内容和反思结果的字典
        """
        try:
            # 第一步：生成初始内容
            initial_content = self._generate_initial_content(prompt, context)
            
            # 第二步：自我反思评估
            reflection_result = self._self_reflect(initial_content, prompt, context)
            
            # 第三步：基于反思结果改进内容
            if reflection_result['needs_improvement']:
                improved_content = self._improve_content(
                    initial_content, 
                    reflection_result['issues'],
                    context
                )
                
                # 再次验证改进效果
                final_reflection = self._self_reflect(improved_content, prompt, context)
                
                return {
                    'final_content': improved_content,
                    'initial_content': initial_content,
                    'initial_reflection': reflection_result,
                    'final_reflection': final_reflection,
                    'improvement_applied': True,
                    'quality_score': final_reflection['overall_quality']
                }
            else:
                return {
                    'final_content': initial_content,
                    'initial_reflection': reflection_result,
                    'improvement_applied': False,
                    'quality_score': reflection_result['overall_quality']
                }
                
        except Exception as e:
            logger.error(f"自我反思生成失败: {e}")
            return {
                'final_content': "",
                'error': str(e),
                'quality_score': 0
            }
    
    def _generate_initial_content(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """生成初始内容"""
        enhanced_prompt = f"""
请根据以下要求生成小说内容：

{prompt}

要求：
1. 内容要有逻辑性和连贯性
2. 语言要生动自然，避免AI痕迹
3. 情节要有张力和吸引力
4. 人物塑造要立体丰满

请生成内容：
"""
        
        if context:
            enhanced_prompt += f"\n上下文信息：\n{json.dumps(context, ensure_ascii=False, indent=2)}"
        
        response = self.llm_client.generate(enhanced_prompt)
        return response.strip()
    
    def _self_reflect(self, content: str, original_prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        对生成内容进行自我反思评估
        
        Returns:
            包含评估结果的字典
        """
        reflection_prompt = f"""
作为一个专业的小说评论家，请对以下生成的小说内容进行全面评估：

【原始要求】
{original_prompt}

【生成内容】
{content}

请从以下8个维度进行评估（每项10分制）：

1. **逻辑连贯性**: 内容前后逻辑是否一致，情节发展是否合理
2. **情感共鸣**: 是否能触动读者情感，有温度感
3. **原创性**: 是否有新颖的创意，避免套路化
4. **人物塑造**: 角色是否立体，有个性特色
5. **语言质量**: 是否自然流畅，无AI痕迹
6. **叙事节奏**: 节奏是否适中，有张有弛
7. **主题深度**: 是否有深层内涵，不流于表面
8. **文化适配**: 是否符合文化背景，真实可信

请按以下JSON格式输出评估结果：
```json
{{
    "scores": {{
        "logic_coherence": 分数,
        "emotional_resonance": 分数,
        "originality": 分数,
        "character_depth": 分数,
        "language_quality": 分数,
        "narrative_rhythm": 分数,
        "theme_depth": 分数,
        "cultural_authenticity": 分数
    }},
    "overall_quality": 总体分数,
    "strengths": ["优点1", "优点2"],
    "issues": ["问题1", "问题2"],
    "needs_improvement": true/false,
    "improvement_suggestions": ["建议1", "建议2"]
}}
```
"""
        
        response = self.llm_client.generate(reflection_prompt)
        
        try:
            # 提取JSON部分
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(1))
            else:
                # 尝试直接解析
                result = json.loads(response)
            
            # 验证和补充结果
            result = self._validate_reflection_result(result)
            return result
            
        except Exception as e:
            logger.error(f"反思结果解析失败: {e}")
            # 返回默认评估
            return {
                'scores': {k: 5.0 for k in ['logic_coherence', 'emotional_resonance', 'originality', 
                          'character_depth', 'language_quality', 'narrative_rhythm', 
                          'theme_depth', 'cultural_authenticity']},
                'overall_quality': 5.0,
                'strengths': [],
                'issues': ["评估解析失败"],
                'needs_improvement': True,
                'improvement_suggestions': ["需要人工检查内容质量"]
            }
    
    def _improve_content(self, content: str, issues: List[str], context: Dict[str, Any] = None) -> str:
        """基于发现的问题改进内容"""
        improvement_prompt = f"""
请根据以下发现的问题，对小说内容进行改进：

【原始内容】
{content}

【发现的问题】
{chr(10).join(f"- {issue}" for issue in issues)}

改进要求：
1. 针对每个问题进行有针对性的修改
2. 保持原有内容的基本结构和情节
3. 提升内容的整体质量和可读性
4. 确保改进后的内容更加生动、自然、有吸引力

请输出改进后的内容：
"""
        
        if context:
            improvement_prompt += f"\n上下文参考：\n{json.dumps(context, ensure_ascii=False, indent=2)}"
        
        improved_content = self.llm_client.generate(improvement_prompt)
        return improved_content.strip()
    
    def _validate_reflection_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """验证和补充反思结果"""
        # 确保所有必要字段存在
        default_result = {
            'scores': {
                'logic_coherence': 5.0,
                'emotional_resonance': 5.0, 
                'originality': 5.0,
                'character_depth': 5.0,
                'language_quality': 5.0,
                'narrative_rhythm': 5.0,
                'theme_depth': 5.0,
                'cultural_authenticity': 5.0
            },
            'overall_quality': 5.0,
            'strengths': [],
            'issues': [],
            'needs_improvement': False,
            'improvement_suggestions': []
        }
        
        # 合并结果
        for key, default_value in default_result.items():
            if key not in result:
                result[key] = default_value
            elif key == 'scores' and isinstance(result[key], dict):
                for score_key, score_default in default_value.items():
                    if score_key not in result[key]:
                        result[key][score_key] = score_default
        
        # 计算总体质量（如果没有提供）
        if 'overall_quality' not in result or not result['overall_quality']:
            scores = result['scores']
            result['overall_quality'] = sum(scores.values()) / len(scores)
        
        # 判断是否需要改进
        if result['overall_quality'] < 7.0 or len(result['issues']) > 0:
            result['needs_improvement'] = True
        
        return result
    
    def batch_reflect_chapters(self, chapter_contents: List[Tuple[int, str]], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """批量反思多个章节"""
        results = {}
        total_score = 0
        improvement_count = 0
        
        for chapter_num, content in chapter_contents:
            prompt = f"请评估第{chapter_num}章的内容质量"
            
            chapter_result = self.generate_with_reflection(prompt, {
                **(context or {}),
                'chapter_number': chapter_num,
                'content': content
            })
            
            results[f'chapter_{chapter_num}'] = chapter_result
            total_score += chapter_result.get('quality_score', 0)
            
            if chapter_result.get('improvement_applied'):
                improvement_count += 1
        
        return {
            'chapter_results': results,
            'summary': {
                'total_chapters': len(chapter_contents),
                'average_quality': total_score / len(chapter_contents) if chapter_contents else 0,
                'improved_chapters': improvement_count,
                'improvement_rate': improvement_count / len(chapter_contents) if chapter_contents else 0
            }
        }
    
    def get_reflection_statistics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """获取反思统计信息"""
        if 'chapter_results' not in results:
            return {}
        
        chapter_results = results['chapter_results']
        
        # 收集所有分数
        all_scores = []
        problem_categories = {}
        
        for chapter_key, chapter_data in chapter_results.items():
            if 'final_reflection' in chapter_data:
                reflection = chapter_data['final_reflection']
                scores = reflection.get('scores', {})
                all_scores.append(scores)
                
                # 统计问题类别
                for issue in reflection.get('issues', []):
                    problem_categories[issue] = problem_categories.get(issue, 0) + 1
        
        if not all_scores:
            return {}
        
        # 计算平均分数
        avg_scores = {}
        for dimension in all_scores[0].keys():
            avg_scores[dimension] = sum(scores[dimension] for scores in all_scores) / len(all_scores)
        
        return {
            'average_scores': avg_scores,
            'common_issues': sorted(problem_categories.items(), key=lambda x: x[1], reverse=True)[:5],
            'total_chapters_analyzed': len(all_scores)
        }


class NovelQualityValidator:
    """小说质量验证器"""
    
    def __init__(self, reflection_engine: SelfReflectionEngine):
        self.reflection_engine = reflection_engine
    
    def validate_novel_coherence(self, chapters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """验证整部小说的连贯性"""
        coherence_issues = []
        chapter_qualities = []
        
        for i, chapter in enumerate(chapters):
            chapter_num = chapter.get('chapter_number', i + 1)
            content = chapter.get('content', '')
            
            if not content:
                coherence_issues.append(f"第{chapter_num}章内容为空")
                continue
            
            # 检查与前一章的连贯性
            if i > 0:
                prev_content = chapters[i-1].get('content', '')
                coherence_score = self._check_chapter_coherence(prev_content, content, chapter_num)
                
                if coherence_score < 7.0:
                    coherence_issues.append(f"第{chapter_num}章与第{chapter_num-1}章连贯性不足")
            
            # 评估单章质量
            reflection_result = self.reflection_engine._self_reflect(
                content, f"评估第{chapter_num}章质量", {'chapter_number': chapter_num}
            )
            
            chapter_qualities.append({
                'chapter': chapter_num,
                'quality_score': reflection_result['overall_quality'],
                'issues': reflection_result['issues']
            })
        
        # 计算整体质量
        avg_quality = sum(cq['quality_score'] for cq in chapter_qualities) / len(chapter_qualities) if chapter_qualities else 0
        
        return {
            'overall_coherence_score': max(0, 10 - len(coherence_issues)),
            'average_quality_score': avg_quality,
            'coherence_issues': coherence_issues,
            'chapter_qualities': chapter_qualities,
            'validation_passed': len(coherence_issues) == 0 and avg_quality >= 7.0
        }
    
    def _check_chapter_coherence(self, prev_content: str, current_content: str, chapter_num: int) -> float:
        """检查章节间连贯性"""
        coherence_prompt = f"""
请评估以下两个连续章节之间的连贯性：

【前一章末尾】
{prev_content[-500:]}  # 取最后500字符

【当前章开头】
{current_content[:500]}  # 取前500字符

评估维度：
1. 情节连续性：是否存在逻辑断层
2. 角色状态连贯性：人物状态是否前后一致
3. 场景转换合理性：场景变化是否自然
4. 时间线连贯性：时间推进是否合理

请给出1-10分的连贯性评分，并简要说明原因。

格式：分数: X.X
原因: [说明]
"""
        
        try:
            response = self.reflection_engine.llm_client.generate(coherence_prompt)
            
            # 提取分数
            score_match = re.search(r'分数:\s*(\d+\.?\d*)', response)
            if score_match:
                return float(score_match.group(1))
            else:
                return 5.0  # 默认分数
                
        except Exception as e:
            logger.error(f"连贯性检查失败: {e}")
            return 5.0
