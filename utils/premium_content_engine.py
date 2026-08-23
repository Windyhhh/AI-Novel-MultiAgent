"""
高质量内容生成引擎
参考《The Anatomy of Story》、《Story Genius》等经典写作理论
结合GPT-3论文、《Language Models are Few-Shot Learners》等技术研究
以及分析了网络优秀小说作品的写作技巧
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from utils import LLMClient, get_logger

logger = get_logger('premium_content_engine')

@dataclass
class ContentQualityMetrics:
    """内容质量指标"""
    literary_score: float  # 文学性评分
    readability_score: float  # 可读性评分
    emotional_depth: float  # 情感深度
    plot_tension: float  # 情节张力
    character_voice: float  # 角色声音
    scene_vividness: float  # 场景生动性
    pacing_score: float  # 节奏控制
    originality: float  # 原创性

class PremiumContentEngine:
    """高质量内容生成引擎"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.quality_analyzer = LiteraryQualityAnalyzer()
        self.writing_techniques = WritingTechniquesLibrary()
        self.emotional_resonance = EmotionalResonanceEngine()
        self.narrative_architect = NarrativeArchitect()
        
    def generate_premium_chapter(self, chapter_plan: Dict[str, Any], 
                                context: Dict[str, Any]) -> Dict[str, Any]:
        """生成高质量章节"""
        logger.info(f"开始生成高质量第{chapter_plan.get('chapter_number')}章")
        
        # 第一阶段：深度分析和准备
        analysis = self._deep_content_analysis(chapter_plan, context)
        
        # 第二阶段：构建叙事架构
        narrative_structure = self.narrative_architect.build_chapter_architecture(
            chapter_plan, context, analysis
        )
        
        # 第三阶段：多层次内容生成
        content_layers = self._generate_layered_content(
            narrative_structure, analysis, context
        )
        
        # 第四阶段：情感共鸣优化
        emotionally_optimized = self.emotional_resonance.enhance_emotional_impact(
            content_layers['base_content'], context, analysis
        )
        
        # 第五阶段：文学技巧应用
        literary_enhanced = self.writing_techniques.apply_advanced_techniques(
            emotionally_optimized, analysis, context
        )
        
        # 第六阶段：质量评估和迭代优化
        final_content, quality_metrics = self._iterative_quality_optimization(
            literary_enhanced, chapter_plan, context, max_iterations=3
        )
        
        return {
            'chapter_number': chapter_plan.get('chapter_number'),
            'content': final_content,
            'word_count': len(final_content),
            'quality_metrics': quality_metrics,
            'narrative_structure': narrative_structure,
            'generation_analysis': analysis,
            'optimization_history': [],  # 优化历史记录
            'generated_at': datetime.now().isoformat(),
            'premium_features': {
                'literary_techniques_applied': self.writing_techniques.get_applied_techniques(),
                'emotional_peaks': self.emotional_resonance.get_emotional_peaks(),
                'narrative_devices': narrative_structure.get('devices', [])
            }
        }
    
    def _deep_content_analysis(self, chapter_plan: Dict[str, Any], 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """深度内容分析"""
        chapter_number = chapter_plan.get('chapter_number', 1)
        
        prompt = f"""
作为资深文学分析师，请深度分析以下章节创作需求：

章节规划：
{json.dumps(chapter_plan, ensure_ascii=False, indent=2)}

故事上下文：
{json.dumps(context.get('recent_summaries', [])[-3:], ensure_ascii=False)}

请从以下维度进行分析：

1. 叙事功能分析：
   - 本章在整体故事结构中的作用
   - 需要推进的核心情节线
   - 角色发展的关键节点

2. 情感弧线设计：
   - 章节情感走向（起承转合）
   - 角色内心冲突和情感变化
   - 读者情感体验设计

3. 写作重点识别：
   - 需要重点描写的场景
   - 关键对话设计要点
   - 细节描写重点区域

4. 文学技巧建议：
   - 适合的叙事视角和技法
   - 修辞手法使用建议
   - 语言风格定位

5. 张力控制策略：
   - 悬念设置点
   - 冲突升级节奏
   - 情节转折时机

返回结构化分析结果。
"""
        
        try:
            analysis_result = self.llm.generate(prompt, max_tokens=3000, temperature=0.7)
            
            return {
                'raw_analysis': analysis_result,
                'chapter_function': self._extract_narrative_function(analysis_result),
                'emotional_arc': self._extract_emotional_arc(analysis_result),
                'writing_focus': self._extract_writing_focus(analysis_result),
                'tension_strategy': self._extract_tension_strategy(analysis_result),
                'quality_targets': self._set_quality_targets(chapter_number, context)
            }
            
        except Exception as e:
            logger.error(f"深度内容分析失败: {e}")
            return self._default_analysis(chapter_plan, context)
    
    def _generate_layered_content(self, narrative_structure: Dict[str, Any], 
                                 analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """多层次内容生成"""
        
        # 第一层：基础故事内容
        base_content = self._generate_base_story(narrative_structure, analysis, context)
        
        # 第二层：场景描写增强
        scene_enhanced = self._enhance_scene_descriptions(base_content, analysis)
        
        # 第三层：对话精雕细琢
        dialogue_refined = self._refine_dialogues(scene_enhanced, analysis, context)
        
        # 第四层：内心独白和心理描写
        psychological_depth = self._add_psychological_depth(dialogue_refined, analysis, context)
        
        return {
            'base_content': base_content,
            'scene_enhanced': scene_enhanced,
            'dialogue_refined': dialogue_refined,
            'psychological_depth': psychological_depth,
            'final_layer': psychological_depth  # 最终版本
        }
    
    def _generate_base_story(self, structure: Dict[str, Any], 
                           analysis: Dict[str, Any], context: Dict[str, Any]) -> str:
        """生成基础故事内容"""
        prompt = f"""
基于以下分析和结构，创作高质量的章节基础内容：

叙事结构：
{json.dumps(structure, ensure_ascii=False)}

创作分析：
{analysis.get('raw_analysis', '')}

上下文：
{json.dumps(context.get('character_states', {}), ensure_ascii=False)}

创作要求：
1. 严格遵循叙事结构安排
2. 体现深度的角色心理
3. 营造生动的场景氛围
4. 保持情节推进的自然性
5. 语言具有文学性和感染力
6. 字数控制在2500-3000字

请创作完整的章节内容，注重：
- 精确的情感表达
- 生动的感官描写
- 有层次的冲突展现
- 自然的情节推进
- 符合角色性格的行为和对话
"""
        
        try:
            base_story = self.llm.generate(prompt, max_tokens=4000, temperature=0.8)
            return base_story
        except Exception as e:
            logger.error(f"生成基础故事失败: {e}")
            return f"第{structure.get('chapter_number', 'X')}章内容生成失败。"
    
    def _enhance_scene_descriptions(self, content: str, analysis: Dict[str, Any]) -> str:
        """增强场景描写"""
        prompt = f"""
请增强以下内容中的场景描写，使其更加生动和有感染力：

原始内容：
{content}

创作分析参考：
{analysis.get('writing_focus', '')}

增强要求：
1. 运用五感描写（视觉、听觉、嗅觉、触觉、味觉）
2. 通过环境烘托情感和氛围
3. 使用具体而非抽象的描述
4. 适度运用比喻、拟人等修辞手法
5. 保持描写与情节的有机结合
6. 避免过度描写影响节奏

请输出场景描写增强后的完整内容。
"""
        
        try:
            enhanced_content = self.llm.generate(prompt, max_tokens=4500, temperature=0.7)
            return enhanced_content
        except Exception as e:
            logger.error(f"场景描写增强失败: {e}")
            return content
    
    def _refine_dialogues(self, content: str, analysis: Dict[str, Any], 
                         context: Dict[str, Any]) -> str:
        """精雕细琢对话"""
        prompt = f"""
请精炼和提升以下内容中的对话质量：

内容：
{content}

角色信息：
{json.dumps(context.get('character_states', {}), ensure_ascii=False)}

对话优化要求：
1. 每个角色的对话都要体现其独特的说话方式
2. 对话要推进情节发展或揭示角色内心
3. 增加对话的潜台词和言外之意
4. 适当运用对话的停顿、省略、重复等技巧
5. 对话要自然流畅，符合情境和角色关系
6. 避免解释性对话，多用展现性对话

参考经典作家的对话写作技巧，如海明威的简洁有力、张爱玲的精妙独特。

请输出对话精炼后的完整内容。
"""
        
        try:
            refined_content = self.llm.generate(prompt, max_tokens=4500, temperature=0.7)
            return refined_content
        except Exception as e:
            logger.error(f"对话精炼失败: {e}")
            return content
    
    def _add_psychological_depth(self, content: str, analysis: Dict[str, Any], 
                               context: Dict[str, Any]) -> str:
        """增加心理深度"""
        prompt = f"""
请为以下内容增加心理描写的深度和层次：

内容：
{content}

情感弧线参考：
{analysis.get('emotional_arc', '')}

心理描写要求：
1. 深入挖掘角色的内心世界和潜意识
2. 展现角色复杂、矛盾的内心冲突
3. 通过内心独白揭示角色动机和恐惧
4. 运用象征和隐喻表达深层心理状态
5. 将心理描写与行为、表情、动作结合
6. 体现人性的复杂性和真实性

参考优秀作品的心理描写技巧，如陀思妥耶夫斯基的深层心理探索。

请输出增加心理深度后的完整内容。
"""
        
        try:
            depth_enhanced = self.llm.generate(prompt, max_tokens=5000, temperature=0.8)
            return depth_enhanced
        except Exception as e:
            logger.error(f"心理深度增强失败: {e}")
            return content
    
    def _iterative_quality_optimization(self, content: str, chapter_plan: Dict[str, Any],
                                      context: Dict[str, Any], max_iterations: int = 3) -> Tuple[str, ContentQualityMetrics]:
        """迭代质量优化"""
        current_content = content
        optimization_history = []
        
        for iteration in range(max_iterations):
            # 评估当前质量
            quality_metrics = self.quality_analyzer.analyze_content_quality(current_content, context)
            optimization_history.append(quality_metrics)
            
            # 如果质量已经很高，停止优化
            if quality_metrics.literary_score > 8.5 and quality_metrics.emotional_depth > 8.0:
                logger.info(f"第{iteration+1}次迭代达到高质量标准，停止优化")
                break
            
            # 识别需要改进的方面
            improvement_areas = self._identify_improvement_areas(quality_metrics)
            
            if not improvement_areas:
                logger.info("无明显改进空间，停止优化")
                break
            
            # 针对性优化
            current_content = self._targeted_optimization(
                current_content, improvement_areas, chapter_plan, context
            )
        
        final_metrics = self.quality_analyzer.analyze_content_quality(current_content, context)
        return current_content, final_metrics
    
    def _targeted_optimization(self, content: str, improvement_areas: List[str],
                             chapter_plan: Dict[str, Any], context: Dict[str, Any]) -> str:
        """针对性优化"""
        optimization_prompt = f"""
请针对以下内容的特定方面进行优化：

需要改进的方面：
{', '.join(improvement_areas)}

内容：
{content}

针对性优化要求：
"""
        
        if '文学性' in improvement_areas:
            optimization_prompt += """
- 提升语言的文学性和艺术性
- 增加修辞手法的运用
- 提高词汇的准确性和表现力
"""
        
        if '情感深度' in improvement_areas:
            optimization_prompt += """
- 深化情感表达和心理描写
- 增强角色内心冲突的复杂性
- 提高情感共鸣度
"""
        
        if '情节张力' in improvement_areas:
            optimization_prompt += """
- 加强冲突的设置和发展
- 优化悬念和转折的时机
- 提高情节的紧张感
"""
        
        if '节奏控制' in improvement_areas:
            optimization_prompt += """
- 调整叙述的快慢节奏
- 平衡动作与反思的比例
- 优化段落和句子的长短搭配
"""
        
        optimization_prompt += "\n请输出优化后的完整内容，确保改进目标方面的质量提升。"
        
        try:
            optimized_content = self.llm.generate(optimization_prompt, max_tokens=5500, temperature=0.7)
            return optimized_content
        except Exception as e:
            logger.error(f"针对性优化失败: {e}")
            return content
    
    def _identify_improvement_areas(self, metrics: ContentQualityMetrics) -> List[str]:
        """识别需要改进的方面"""
        areas = []
        threshold = 7.0  # 质量阈值
        
        if metrics.literary_score < threshold:
            areas.append('文学性')
        if metrics.emotional_depth < threshold:
            areas.append('情感深度')
        if metrics.plot_tension < threshold:
            areas.append('情节张力')
        if metrics.pacing_score < threshold:
            areas.append('节奏控制')
        if metrics.scene_vividness < threshold:
            areas.append('场景描写')
        if metrics.character_voice < threshold:
            areas.append('角色声音')
        
        return areas

class LiteraryQualityAnalyzer:
    """文学质量分析器"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def analyze_content_quality(self, content: str, context: Dict[str, Any]) -> ContentQualityMetrics:
        """分析内容质量"""
        prompt = f"""
作为文学评论专家，请从以下维度评估内容质量（1-10分）：

内容：
{content}

评估维度：
1. 文学性 - 语言的艺术性、修辞运用、表达精准度
2. 可读性 - 语言流畅度、理解难度、阅读愉悦感
3. 情感深度 - 情感表达的深度、角色心理复杂性、共鸣度
4. 情节张力 - 冲突设置、悬念营造、转折效果
5. 角色声音 - 角色个性化表达、对话真实性、性格体现
6. 场景生动性 - 描写的画面感、感官体验、氛围营造
7. 节奏控制 - 快慢节奏搭配、段落结构、叙述流畅度
8. 原创性 - 表达方式新颖度、情节创新性、独特视角

请返回JSON格式评分：
{{
    "literary_score": 分数,
    "readability_score": 分数,
    "emotional_depth": 分数,
    "plot_tension": 分数,
    "character_voice": 分数,
    "scene_vividness": 分数,
    "pacing_score": 分数,
    "originality": 分数,
    "overall_assessment": "整体评价",
    "strengths": ["优点1", "优点2"],
    "improvements": ["改进建议1", "改进建议2"]
}}
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=1500, temperature=0.3)
            result = json.loads(response)
            
            return ContentQualityMetrics(
                literary_score=result.get('literary_score', 7.0),
                readability_score=result.get('readability_score', 7.0),
                emotional_depth=result.get('emotional_depth', 7.0),
                plot_tension=result.get('plot_tension', 7.0),
                character_voice=result.get('character_voice', 7.0),
                scene_vividness=result.get('scene_vividness', 7.0),
                pacing_score=result.get('pacing_score', 7.0),
                originality=result.get('originality', 7.0)
            )
        
        except Exception as e:
            logger.error(f"质量分析失败: {e}")
            # 返回默认评分
            return ContentQualityMetrics(7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0)

class WritingTechniquesLibrary:
    """写作技巧库"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.applied_techniques = []
        
        # 经典写作技巧库
        self.techniques = {
            '冰山理论': '海明威式的简洁表达，用少量文字暗示深层含义',
            '意识流': '展现角色内心复杂的思维过程',
            '蒙太奇': '通过场景切换和镜头感营造效果',
            '对比反衬': '通过对立元素突出主题',
            '伏笔照应': '前文埋伏笔，后文有照应',
            '欲扬先抑': '先贬抑后褒扬，增强表达效果',
            '白描': '简练的笔墨，不加渲染地描写',
            '细节刻画': '通过具体细节展现人物和环境'
        }
    
    def apply_advanced_techniques(self, content: str, analysis: Dict[str, Any], 
                                context: Dict[str, Any]) -> str:
        """应用高级写作技巧"""
        
        # 选择适合的技巧
        suitable_techniques = self._select_suitable_techniques(content, analysis)
        
        enhanced_content = content
        for technique in suitable_techniques:
            enhanced_content = self._apply_single_technique(
                enhanced_content, technique, analysis, context
            )
            self.applied_techniques.append(technique)
        
        return enhanced_content
    
    def _select_suitable_techniques(self, content: str, analysis: Dict[str, Any]) -> List[str]:
        """选择合适的写作技巧"""
        selected = []
        
        # 根据内容特点选择技巧
        if '对话' in content and len(re.findall(r'"[^"]*"', content)) > 5:
            selected.append('冰山理论')  # 对话丰富时适用冰山理论
        
        if '内心' in content or '想到' in content:
            selected.append('意识流')  # 有内心描写时适用意识流
        
        if len(content) > 2000:
            selected.append('细节刻画')  # 长内容适合细节刻画
            selected.append('蒙太奇')  # 长内容需要镜头感
        
        return selected[:2]  # 限制同时应用的技巧数量
    
    def _apply_single_technique(self, content: str, technique: str,
                               analysis: Dict[str, Any], context: Dict[str, Any]) -> str:
        """应用单一写作技巧"""
        technique_desc = self.techniques.get(technique, '')
        
        prompt = f"""
请运用"{technique}"写作技法优化以下内容：

技法说明：{technique_desc}

内容：
{content}

优化要求：
1. 自然融入该技法，不生硬
2. 保持原有情节和人物不变
3. 提升内容的文学性和表现力
4. 确保技法运用恰到好处

请输出运用该技法后的完整内容。
"""
        
        try:
            enhanced = self.llm.generate(prompt, max_tokens=5000, temperature=0.7)
            return enhanced
        except Exception as e:
            logger.error(f"应用写作技巧{technique}失败: {e}")
            return content
    
    def get_applied_techniques(self) -> List[str]:
        """获取已应用的技巧"""
        return self.applied_techniques.copy()

class EmotionalResonanceEngine:
    """情感共鸣引擎"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.emotional_peaks = []
    
    def enhance_emotional_impact(self, content: str, context: Dict[str, Any], 
                               analysis: Dict[str, Any]) -> str:
        """增强情感冲击力"""
        
        # 识别情感关键点
        emotional_points = self._identify_emotional_points(content)
        
        # 分析情感弧线
        emotional_arc = self._analyze_emotional_arc(content, analysis)
        
        # 增强情感表达
        enhanced_content = self._enhance_emotional_expression(
            content, emotional_points, emotional_arc, context
        )
        
        return enhanced_content
    
    def _identify_emotional_points(self, content: str) -> List[Dict[str, Any]]:
        """识别情感关键点"""
        prompt = f"""
请识别以下内容中的情感关键点：

内容：
{content}

请识别出：
1. 情感高潮点（最激烈的情感时刻）
2. 情感转折点（情感发生变化的时刻）
3. 情感低谷点（情感最低沉的时刻）
4. 情感冲突点（内心矛盾激烈的时刻）

返回JSON格式：
{{
    "emotional_peaks": [
        {{"type": "高潮/转折/低谷/冲突", "position": "在内容中的大致位置", "description": "情感描述"}}
    ]
}}
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=1000, temperature=0.3)
            result = json.loads(response)
            self.emotional_peaks = result.get('emotional_peaks', [])
            return self.emotional_peaks
        except Exception as e:
            logger.error(f"识别情感关键点失败: {e}")
            return []

class NarrativeArchitect:
    """叙事架构师"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def build_chapter_architecture(self, chapter_plan: Dict[str, Any], 
                                 context: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """构建章节叙事架构"""
        
        prompt = f"""
作为叙事结构专家，请为以下章节设计精密的叙事架构：

章节规划：
{json.dumps(chapter_plan, ensure_ascii=False)}

故事上下文：
{json.dumps(context.get('recent_summaries', [])[-2:], ensure_ascii=False)}

分析结果：
{analysis.get('chapter_function', '')}

请设计包含以下元素的叙事架构：

1. 章节结构：
   - 开场（Hook）- 如何抓住读者注意力
   - 发展（Development）- 情节如何推进
   - 转折（Turning Point）- 关键转折时刻
   - 高潮（Climax）- 章节情感/冲突高潮
   - 结尾（Resolution）- 如何为下章铺垫

2. 叙事技法：
   - 叙述视角（第一人称/第三人称限制/全知等）
   - 时间处理（线性/倒叙/插叙等）
   - 空间安排（场景切换/聚焦等）

3. 节奏控制：
   - 快节奏部分（动作、对话）
   - 慢节奏部分（描写、思考）
   - 节奏变化的转换点

返回详细的架构设计。
"""
        
        try:
            architecture = self.llm.generate(prompt, max_tokens=2500, temperature=0.6)
            return {
                'raw_architecture': architecture,
                'structure_elements': self._parse_structure_elements(architecture),
                'narrative_devices': self._extract_narrative_devices(architecture),
                'pacing_plan': self._extract_pacing_plan(architecture)
            }
        except Exception as e:
            logger.error(f"构建叙事架构失败: {e}")
            return {'raw_architecture': '基础章节架构', 'structure_elements': []}
