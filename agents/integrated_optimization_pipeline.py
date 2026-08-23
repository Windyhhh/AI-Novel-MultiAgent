"""
一条龙智能体协作优化系统
整合所有智能体，实现小说的全方位优化流水线
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import LLMClient, get_logger, Storage
from utils.context_coherence_engine import ContextCoherenceEngine
from utils.premium_content_engine import PremiumContentEngine
from utils.dynamic_learning_engine import DynamicLearningEngine
from utils.self_reflection_engine import SelfReflectionEngine
from utils.multimodal_generator import MultimodalGenerator
from utils.intelligent_dialogue_system import CharacterDialogueEngine, EmotionalDialogueGenerator
from utils.quality_analyzer import QualityAnalyzer
from utils.text_humanizer import TextHumanizer
from utils.style_optimizer import StyleOptimizer

logger = get_logger('integrated_optimization_pipeline')

class IntegratedOptimizationPipeline:
    """一条龙智能体协作优化系统"""
    
    def __init__(self):
        self.storage = Storage()
        self.llm = LLMClient()
        
        # 初始化所有引擎和智能体
        self._initialize_engines()
        self._initialize_agents()
        
        # 优化流水线配置
        self.pipeline_stages = [
            'initial_analysis',      # 初始分析
            'content_optimization',  # 内容优化
            'coherence_check',      # 连贯性检查
            'dialogue_optimization', # 对话优化
            'quality_enhancement',  # 质量增强
            'style_refinement',     # 风格精炼
            'final_validation',     # 最终验证
            'multimodal_enrichment' # 多模态丰富
        ]
        
        logger.info("一条龙优化系统初始化完成")
    
    def _initialize_engines(self):
        """初始化所有引擎"""
        self.context_engine = ContextCoherenceEngine()
        self.premium_engine = PremiumContentEngine()
        self.learning_engine = DynamicLearningEngine()
        self.reflection_engine = SelfReflectionEngine(self.llm)
        self.multimodal_generator = MultimodalGenerator(self.llm)
        self.quality_analyzer = QualityAnalyzer()
        self.text_humanizer = TextHumanizer(self.llm)
        self.style_optimizer = StyleOptimizer(self.llm)
        self.dialogue_engine = CharacterDialogueEngine(self.llm)
        self.emotional_dialogue = EmotionalDialogueGenerator(self.llm)
    
    def _initialize_agents(self):
        """初始化所有智能体"""
        from .agent_factory import AgentFactory
        from .agent_orchestrator import AgentOrchestrator
        
        self.agent_factory = AgentFactory()
        self.agent_orchestrator = AgentOrchestrator()
        
        # 获取所有可用智能体
        self.available_agents = self.agent_factory.list_available_agents()
        logger.info(f"可用智能体: {self.available_agents['registered_agents']}")
    
    def optimize_entire_novel(self, optimization_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """优化整部小说的一条龙流程"""
        logger.info("🚀 启动一条龙小说优化系统")
        
        if optimization_config is None:
            optimization_config = self._get_default_optimization_config()
        
        # 获取所有章节
        all_chapters = self.storage.get_all_chapters()
        if not all_chapters:
            return {
                'success': False,
                'error': '未找到任何章节',
                'stage': 'initialization'
            }
        
        chapter_numbers = [ch['number'] if 'number' in ch else ch['chapter_number'] for ch in all_chapters]
        
        optimization_result = {
            'success': False,
            'total_chapters': len(chapter_numbers),
            'optimized_chapters': 0,
            'failed_chapters': 0,
            'stage_results': {},
            'overall_improvements': [],
            'quality_improvement': 0,
            'start_time': datetime.now().isoformat(),
            'config': optimization_config
        }
        
        try:
            # 执行优化流水线
            for stage in self.pipeline_stages:
                logger.info(f"📝 执行阶段: {stage}")
                
                stage_result = self._execute_stage(stage, chapter_numbers, optimization_config)
                optimization_result['stage_results'][stage] = stage_result
                
                if not stage_result.get('success', False):
                    logger.warning(f"阶段 {stage} 执行有问题，但继续执行后续阶段")
            
            # 计算最终结果
            optimization_result = self._calculate_final_results(optimization_result, chapter_numbers)
            
            # 生成优化报告
            self._generate_optimization_report(optimization_result)
            
            logger.info("✅ 一条龙小说优化完成")
            return optimization_result
            
        except Exception as e:
            logger.error(f"一条龙优化失败: {e}")
            optimization_result['error'] = str(e)
            return optimization_result
    
    def _get_default_optimization_config(self) -> Dict[str, Any]:
        """获取默认优化配置"""
        return {
            'target_quality_score': 8.5,
            'optimization_intensity': 'comprehensive',
            'preserve_style': True,
            'enhance_dialogues': True,
            'improve_coherence': True,
            'solve_ai_problems': True,
            'add_multimodal': False,
            'max_parallel_chapters': 3,
            'skip_high_quality': True,
            'quality_threshold': 7.5
        }
    
    def _execute_stage(self, stage: str, chapter_numbers: List[int], config: Dict[str, Any]) -> Dict[str, Any]:
        """执行特定优化阶段"""
        stage_methods = {
            'initial_analysis': self._stage_initial_analysis,
            'content_optimization': self._stage_content_optimization,
            'coherence_check': self._stage_coherence_check,
            'dialogue_optimization': self._stage_dialogue_optimization,
            'quality_enhancement': self._stage_quality_enhancement,
            'style_refinement': self._stage_style_refinement,
            'final_validation': self._stage_final_validation,
            'multimodal_enrichment': self._stage_multimodal_enrichment
        }
        
        method = stage_methods.get(stage)
        if not method:
            return {'success': False, 'error': f'未知阶段: {stage}'}
        
        try:
            return method(chapter_numbers, config)
        except Exception as e:
            logger.error(f"阶段 {stage} 执行失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def _stage_initial_analysis(self, chapter_numbers: List[int], config: Dict[str, Any]) -> Dict[str, Any]:
        """阶段1: 初始分析"""
        logger.info("🔍 执行初始分析阶段")
        
        analysis_results = {
            'chapter_qualities': {},
            'overall_assessment': {},
            'optimization_plan': {},
            'priority_chapters': []
        }
        
        # 分析每个章节的质量
        for ch_num in chapter_numbers[:10]:  # 限制分析前10章避免过长
            chapter_data = self.storage.load_chapter(ch_num)
            if not chapter_data:
                continue
                
            content = chapter_data.get('content', '')
            if not content:
                continue
            
            # 使用质量分析器
            quality_analysis = self.quality_analyzer.analyze(content)
            
            # 使用动态学习引擎获取详细报告
            context = {
                'chapter_number': ch_num,
                'genre': '通用',
                'total_chapters': len(chapter_numbers)
            }
            
            detailed_report = self.learning_engine.get_quality_report(content, context)
            
            chapter_quality = {
                'basic_quality': quality_analysis,
                'detailed_report': detailed_report,
                'needs_optimization': quality_analysis.get('overall_score', 0) < config.get('quality_threshold', 7.5)
            }
            
            analysis_results['chapter_qualities'][ch_num] = chapter_quality
            
            # 标记优先章节
            if chapter_quality['needs_optimization']:
                analysis_results['priority_chapters'].append(ch_num)
        
        # 生成整体评估
        if analysis_results['chapter_qualities']:
            scores = [cq['basic_quality'].get('overall_score', 0) 
                     for cq in analysis_results['chapter_qualities'].values()]
            analysis_results['overall_assessment'] = {
                'average_quality': sum(scores) / len(scores),
                'chapters_analyzed': len(analysis_results['chapter_qualities']),
                'chapters_need_optimization': len(analysis_results['priority_chapters'])
            }
        
        # 生成优化计划
        analysis_results['optimization_plan'] = self._generate_optimization_plan(analysis_results, config)
        
        logger.info(f"初始分析完成，分析了{len(analysis_results['chapter_qualities'])}章，"
                   f"{len(analysis_results['priority_chapters'])}章需要优化")
        
        return {
            'success': True,
            'results': analysis_results,
            'message': f'分析了{len(analysis_results["chapter_qualities"])}章'
        }
    
    def _stage_content_optimization(self, chapter_numbers: List[int], config: Dict[str, Any]) -> Dict[str, Any]:
        """阶段2: 内容优化"""
        logger.info("⚡ 执行内容优化阶段")
        
        optimization_results = {
            'optimized_chapters': [],
            'skipped_chapters': [],
            'failed_chapters': [],
            'improvements_applied': []
        }
        
        # 使用8大问题解决方案优化内容
        target_chapters = chapter_numbers[:config.get('max_parallel_chapters', 3)]
        
        for ch_num in target_chapters:
            chapter_data = self.storage.load_chapter(ch_num)
            if not chapter_data:
                optimization_results['failed_chapters'].append({
                    'chapter': ch_num,
                    'error': '章节不存在'
                })
                continue
            
            content = chapter_data.get('content', '')
            if not content:
                optimization_results['failed_chapters'].append({
                    'chapter': ch_num,
                    'error': '章节内容为空'
                })
                continue
            
            # 检查是否需要优化
            if config.get('skip_high_quality', True):
                quality = self.quality_analyzer.analyze(content)
                if quality.get('overall_score', 0) >= config.get('quality_threshold', 7.5):
                    optimization_results['skipped_chapters'].append({
                        'chapter': ch_num,
                        'reason': '质量已达标'
                    })
                    continue
            
            # 构建优化上下文
            context = {
                'chapter_number': ch_num,
                'genre': '通用',
                'total_chapters': len(chapter_numbers)
            }
            
            # 使用8大问题解决方案
            if config.get('solve_ai_problems', True):
                solution_result = self.learning_engine.solve_core_problems(
                    content, context, list(range(1, 9))
                )
                
                if solution_result['success']:
                    # 更新章节
                    updated_data = chapter_data.copy()
                    updated_data['content'] = solution_result['improved_content']
                    updated_data['word_count'] = len(solution_result['improved_content'])
                    updated_data['content_optimized'] = True
                    updated_data['optimization_timestamp'] = datetime.now().isoformat()
                    
                    self.storage.update_chapter(ch_num, updated_data)
                    
                    optimization_results['optimized_chapters'].append({
                        'chapter': ch_num,
                        'improvements': solution_result['applied_solutions'],
                        'improvement_score': solution_result['overall_improvement']
                    })
                    
                    optimization_results['improvements_applied'].extend(solution_result['applied_solutions'])
                else:
                    optimization_results['failed_chapters'].append({
                        'chapter': ch_num,
                        'error': '8大问题解决失败'
                    })
        
        success_count = len(optimization_results['optimized_chapters'])
        total_count = len(target_chapters)
        
        logger.info(f"内容优化完成，成功优化{success_count}/{total_count}章")
        
        return {
            'success': success_count > 0,
            'results': optimization_results,
            'message': f'优化了{success_count}/{total_count}章'
        }
    
    def _stage_coherence_check(self, chapter_numbers: List[int], config: Dict[str, Any]) -> Dict[str, Any]:
        """阶段3: 连贯性检查"""
        logger.info("🔗 执行连贯性检查阶段")
        
        if not config.get('improve_coherence', True):
            return {
                'success': True,
                'results': {'skipped': True},
                'message': '连贯性检查已跳过'
            }
        
        # 使用上下文连贯性引擎检查整体连贯性
        coherence_results = self.agent_orchestrator.check_novel_coherence(chapter_numbers[:10])
        
        coherence_summary = {
            'overall_coherence_score': coherence_results.get('overall_coherence_score', 0),
            'character_coherence': coherence_results.get('character_coherence', 0),
            'plot_coherence': coherence_results.get('plot_coherence', 0),
            'timeline_coherence': coherence_results.get('timeline_coherence', 0),
            'issues_found': coherence_results.get('issues', []),
            'suggestions': coherence_results.get('suggestions', [])
        }
        
        # 如果连贯性评分较低，尝试改进
        if coherence_summary['overall_coherence_score'] < 7.0:
            logger.info("连贯性评分较低，尝试改进...")
            
            improvement_results = []
            for ch_num in chapter_numbers[:5]:  # 限制改进前5章
                chapter_data = self.storage.load_chapter(ch_num)
                if not chapter_data:
                    continue
                
                content = chapter_data.get('content', '')
                if not content:
                    continue
                
                # 使用上下文连贯性引擎改进
                try:
                    full_context = self.agent_orchestrator.context_manager.get_full_context()
                    improved_content = self.context_engine.ensure_chapter_coherence(
                        content=content,
                        chapter_number=ch_num,
                        novel_context=full_context,
                        storage=self.storage
                    )
                    
                    if improved_content and improved_content != content:
                        # 更新章节
                        updated_data = chapter_data.copy()
                        updated_data['content'] = improved_content
                        updated_data['word_count'] = len(improved_content)
                        updated_data['coherence_improved'] = True
                        
                        self.storage.update_chapter(ch_num, updated_data)
                        improvement_results.append(ch_num)
                        
                except Exception as e:
                    logger.warning(f"第{ch_num}章连贯性改进失败: {e}")
            
            coherence_summary['improved_chapters'] = improvement_results
        
        logger.info(f"连贯性检查完成，总体评分: {coherence_summary['overall_coherence_score']:.1f}/10")
        
        return {
            'success': True,
            'results': coherence_summary,
            'message': f'连贯性评分: {coherence_summary["overall_coherence_score"]:.1f}/10'
        }
    
    def _stage_dialogue_optimization(self, chapter_numbers: List[int], config: Dict[str, Any]) -> Dict[str, Any]:
        """阶段4: 对话优化"""
        logger.info("💬 执行对话优化阶段")
        
        if not config.get('enhance_dialogues', True):
            return {
                'success': True,
                'results': {'skipped': True},
                'message': '对话优化已跳过'
            }
        
        from utils.intelligent_dialogue_system import DialogueOptimizationEngine
        optimization_engine = DialogueOptimizationEngine(self.llm)
        
        dialogue_results = {
            'chapters_processed': 0,
            'dialogues_optimized': 0,
            'optimization_details': []
        }
        
        # 处理前几章的对话
        for ch_num in chapter_numbers[:5]:
            chapter_data = self.storage.load_chapter(ch_num)
            if not chapter_data:
                continue
            
            content = chapter_data.get('content', '')
            if not content:
                continue
            
            # 提取对话内容
            dialogue_sections = self._extract_dialogues(content)
            if not dialogue_sections:
                continue
            
            dialogue_results['chapters_processed'] += 1
            optimized_content = content
            chapter_optimized = False
            
            # 优化每个对话
            for dialogue in dialogue_sections[:3]:  # 限制处理前3个对话
                dialogue_data = {
                    'dialogue': dialogue,
                    'optimization_goals': ['naturalness', 'emotion', 'personality'],
                    'character_profile': {},
                    'emotional_context': {},
                    'scene_context': {}
                }
                
                try:
                    opt_result = optimization_engine.optimize_dialogue_comprehensive(dialogue_data)
                    
                    if opt_result.get('optimized_dialogue') and opt_result['optimized_dialogue'] != dialogue:
                        optimized_content = optimized_content.replace(
                            dialogue, opt_result['optimized_dialogue']
                        )
                        dialogue_results['dialogues_optimized'] += 1
                        chapter_optimized = True
                        
                        dialogue_results['optimization_details'].append({
                            'chapter': ch_num,
                            'original': dialogue[:100] + '...',
                            'optimized': opt_result['optimized_dialogue'][:100] + '...',
                            'improvements': opt_result.get('applied_optimizations', [])
                        })
                        
                except Exception as e:
                    logger.warning(f"对话优化失败: {e}")
            
            # 如果有优化，更新章节
            if chapter_optimized:
                updated_data = chapter_data.copy()
                updated_data['content'] = optimized_content
                updated_data['word_count'] = len(optimized_content)
                updated_data['dialogue_optimized'] = True
                
                self.storage.update_chapter(ch_num, updated_data)
        
        logger.info(f"对话优化完成，处理了{dialogue_results['chapters_processed']}章，"
                   f"优化了{dialogue_results['dialogues_optimized']}个对话")
        
        return {
            'success': True,
            'results': dialogue_results,
            'message': f'优化了{dialogue_results["dialogues_optimized"]}个对话'
        }
    
    def _stage_quality_enhancement(self, chapter_numbers: List[int], config: Dict[str, Any]) -> Dict[str, Any]:
        """阶段5: 质量增强"""
        logger.info("✨ 执行质量增强阶段")
        
        enhancement_results = {
            'enhanced_chapters': [],
            'quality_improvements': [],
            'average_improvement': 0
        }
        
        improvements = []
        
        # 使用高质量内容引擎增强内容
        for ch_num in chapter_numbers[:3]:  # 限制增强前3章
            chapter_data = self.storage.load_chapter(ch_num)
            if not chapter_data:
                continue
            
            content = chapter_data.get('content', '')
            if not content:
                continue
            
            # 使用高质量内容引擎
            try:
                context = {
                    'genre': '通用',
                    'chapter_number': ch_num,
                    'optimization_focus': 'quality'
                }
                
                enhanced_content = self.premium_engine.enhance_existing_content(
                    content=content,
                    genre=context.get('genre', '通用'),
                    context_info=context
                )
                
                if enhanced_content and enhanced_content != content:
                    # 验证质量改进
                    original_quality = self.quality_analyzer.analyze(content)
                    enhanced_quality = self.quality_analyzer.analyze(enhanced_content)
                    
                    quality_improvement = enhanced_quality.get('overall_score', 0) - original_quality.get('overall_score', 0)
                    
                    if quality_improvement > 0.2:  # 只有显著改进才更新
                        updated_data = chapter_data.copy()
                        updated_data['content'] = enhanced_content
                        updated_data['word_count'] = len(enhanced_content)
                        updated_data['quality_enhanced'] = True
                        updated_data['quality_improvement'] = quality_improvement
                        
                        self.storage.update_chapter(ch_num, updated_data)
                        
                        enhancement_results['enhanced_chapters'].append(ch_num)
                        improvements.append(quality_improvement)
                        
                        enhancement_results['quality_improvements'].append({
                            'chapter': ch_num,
                            'before_score': original_quality.get('overall_score', 0),
                            'after_score': enhanced_quality.get('overall_score', 0),
                            'improvement': quality_improvement
                        })
                        
            except Exception as e:
                logger.warning(f"第{ch_num}章质量增强失败: {e}")
        
        if improvements:
            enhancement_results['average_improvement'] = sum(improvements) / len(improvements)
        
        logger.info(f"质量增强完成，增强了{len(enhancement_results['enhanced_chapters'])}章，"
                   f"平均提升{enhancement_results['average_improvement']:.2f}分")
        
        return {
            'success': len(enhancement_results['enhanced_chapters']) > 0,
            'results': enhancement_results,
            'message': f'增强了{len(enhancement_results["enhanced_chapters"])}章'
        }
    
    def _stage_style_refinement(self, chapter_numbers: List[int], config: Dict[str, Any]) -> Dict[str, Any]:
        """阶段6: 风格精炼"""
        logger.info("🎨 执行风格精炼阶段")
        
        if not config.get('preserve_style', True):
            return {
                'success': True,
                'results': {'skipped': True},
                'message': '风格精炼已跳过（保持原风格）'
            }
        
        refinement_results = {
            'refined_chapters': [],
            'style_improvements': [],
            'humanization_results': []
        }
        
        # 风格优化和人性化处理
        for ch_num in chapter_numbers[:3]:  # 限制精炼前3章
            chapter_data = self.storage.load_chapter(ch_num)
            if not chapter_data:
                continue
            
            content = chapter_data.get('content', '')
            if not content:
                continue
            
            try:
                # 先进行人性化处理
                humanize_result = self.text_humanizer.humanize(content, aggressive=False)
                humanized_content = humanize_result.get('humanized_text', content)
                
                # 再进行风格优化
                style_config = {
                    'vivid_description': True,
                    'dialogue_variation': True,
                    'rhythm_adjustment': True,
                    'expression_personalization': True
                }
                
                style_result = self.style_optimizer.optimize(humanized_content, style_config)
                refined_content = style_result.get('optimized_text', humanized_content)
                
                # 检查改进效果
                if refined_content != content:
                    # 验证AI特征降低
                    original_analysis = self.quality_analyzer.analyze(content)
                    refined_analysis = self.quality_analyzer.analyze(refined_content)
                    
                    original_ai_score = original_analysis.get('ai_patterns', {}).get('ai_score', 10)
                    refined_ai_score = refined_analysis.get('ai_patterns', {}).get('ai_score', 10)
                    
                    if refined_ai_score < original_ai_score or refined_analysis.get('overall_score', 0) > original_analysis.get('overall_score', 0):
                        updated_data = chapter_data.copy()
                        updated_data['content'] = refined_content
                        updated_data['word_count'] = len(refined_content)
                        updated_data['style_refined'] = True
                        updated_data['humanization_applied'] = True
                        
                        self.storage.update_chapter(ch_num, updated_data)
                        
                        refinement_results['refined_chapters'].append(ch_num)
                        
                        refinement_results['style_improvements'].append({
                            'chapter': ch_num,
                            'ai_score_reduction': original_ai_score - refined_ai_score,
                            'quality_improvement': refined_analysis.get('overall_score', 0) - original_analysis.get('overall_score', 0)
                        })
                        
                        refinement_results['humanization_results'].append({
                            'chapter': ch_num,
                            'human_score_improvement': humanize_result.get('human_likeness_improvement', 0),
                            'techniques_applied': humanize_result.get('techniques_applied', [])
                        })
                
            except Exception as e:
                logger.warning(f"第{ch_num}章风格精炼失败: {e}")
        
        logger.info(f"风格精炼完成，精炼了{len(refinement_results['refined_chapters'])}章")
        
        return {
            'success': len(refinement_results['refined_chapters']) > 0,
            'results': refinement_results,
            'message': f'精炼了{len(refinement_results["refined_chapters"])}章'
        }
    
    def _stage_final_validation(self, chapter_numbers: List[int], config: Dict[str, Any]) -> Dict[str, Any]:
        """阶段7: 最终验证"""
        logger.info("🔍 执行最终验证阶段")
        
        validation_results = {
            'validated_chapters': 0,
            'quality_scores': {},
            'overall_assessment': {},
            'validation_passed': False
        }
        
        quality_scores = []
        
        # 验证优化后的质量
        for ch_num in chapter_numbers[:10]:  # 验证前10章
            chapter_data = self.storage.load_chapter(ch_num)
            if not chapter_data:
                continue
            
            content = chapter_data.get('content', '')
            if not content:
                continue
            
            # 使用质量分析器进行最终验证
            final_quality = self.quality_analyzer.analyze(content)
            quality_score = final_quality.get('overall_score', 0)
            
            validation_results['quality_scores'][ch_num] = {
                'score': quality_score,
                'level': self._get_quality_level(quality_score),
                'ai_patterns': final_quality.get('ai_patterns', {}),
                'optimization_history': {
                    'content_optimized': chapter_data.get('content_optimized', False),
                    'coherence_improved': chapter_data.get('coherence_improved', False),
                    'dialogue_optimized': chapter_data.get('dialogue_optimized', False),
                    'quality_enhanced': chapter_data.get('quality_enhanced', False),
                    'style_refined': chapter_data.get('style_refined', False)
                }
            }
            
            quality_scores.append(quality_score)
            validation_results['validated_chapters'] += 1
        
        # 生成整体评估
        if quality_scores:
            average_quality = sum(quality_scores) / len(quality_scores)
            validation_results['overall_assessment'] = {
                'average_quality': average_quality,
                'chapters_validated': validation_results['validated_chapters'],
                'target_quality': config.get('target_quality_score', 8.5),
                'validation_passed': average_quality >= config.get('target_quality_score', 8.5)
            }
            validation_results['validation_passed'] = validation_results['overall_assessment']['validation_passed']
        
        logger.info(f"最终验证完成，验证了{validation_results['validated_chapters']}章，"
                   f"平均质量: {validation_results['overall_assessment'].get('average_quality', 0):.1f}/10")
        
        return {
            'success': True,
            'results': validation_results,
            'message': f'验证了{validation_results["validated_chapters"]}章'
        }
    
    def _stage_multimodal_enrichment(self, chapter_numbers: List[int], config: Dict[str, Any]) -> Dict[str, Any]:
        """阶段8: 多模态丰富"""
        logger.info("🎨 执行多模态丰富阶段")
        
        if not config.get('add_multimodal', False):
            return {
                'success': True,
                'results': {'skipped': True},
                'message': '多模态丰富已跳过'
            }
        
        enrichment_results = {
            'enriched_chapters': [],
            'multimodal_elements': {},
            'total_elements_added': 0
        }
        
        # 为前几章添加多模态元素
        for ch_num in chapter_numbers[:3]:  # 限制处理前3章
            chapter_data = self.storage.load_chapter(ch_num)
            if not chapter_data:
                continue
            
            content = chapter_data.get('content', '')
            if not content:
                continue
            
            try:
                # 生成图像描述
                image_descriptions = self.multimodal_generator._generate_image_descriptions(
                    content, {'image_style': 'illustration', 'max_images': 2}
                )
                
                # 生成音频描述
                audio_descriptions = self.multimodal_generator._generate_audio_descriptions(
                    content, {'audio_elements': ['background_music', 'sound_effects']}
                )
                
                if image_descriptions or audio_descriptions:
                    # 更新章节数据
                    multimodal_elements = {
                        'images': image_descriptions,
                        'audio': audio_descriptions
                    }
                    
                    updated_data = chapter_data.copy()
                    updated_data['multimodal_elements'] = multimodal_elements
                    updated_data['multimodal_enriched'] = True
                    
                    self.storage.update_chapter(ch_num, updated_data)
                    
                    enrichment_results['enriched_chapters'].append(ch_num)
                    enrichment_results['multimodal_elements'][ch_num] = multimodal_elements
                    enrichment_results['total_elements_added'] += len(image_descriptions) + len(audio_descriptions)
                    
            except Exception as e:
                logger.warning(f"第{ch_num}章多模态丰富失败: {e}")
        
        logger.info(f"多模态丰富完成，丰富了{len(enrichment_results['enriched_chapters'])}章，"
                   f"添加了{enrichment_results['total_elements_added']}个元素")
        
        return {
            'success': len(enrichment_results['enriched_chapters']) > 0,
            'results': enrichment_results,
            'message': f'丰富了{len(enrichment_results["enriched_chapters"])}章'
        }
    
    def _generate_optimization_plan(self, analysis_results: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """生成优化计划"""
        plan = {
            'priority_chapters': analysis_results.get('priority_chapters', []),
            'optimization_strategies': [],
            'expected_improvements': {},
            'resource_estimation': {}
        }
        
        # 根据分析结果制定策略
        if analysis_results['priority_chapters']:
            plan['optimization_strategies'].append('content_optimization')
            plan['optimization_strategies'].append('quality_enhancement')
        
        if config.get('improve_coherence', True):
            plan['optimization_strategies'].append('coherence_check')
        
        if config.get('enhance_dialogues', True):
            plan['optimization_strategies'].append('dialogue_optimization')
        
        if config.get('preserve_style', True):
            plan['optimization_strategies'].append('style_refinement')
        
        # 估算资源需求
        total_chapters = len(analysis_results.get('priority_chapters', []))
        plan['resource_estimation'] = {
            'estimated_time_minutes': total_chapters * 5,  # 每章约5分钟
            'chapters_to_process': total_chapters,
            'parallel_processing': config.get('max_parallel_chapters', 3)
        }
        
        return plan
    
    def _extract_dialogues(self, content: str) -> List[str]:
        """从内容中提取对话"""
        dialogues = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            # 检查是否为对话行
            if ('：' in line or '「' in line or '"' in line) and len(line) > 5:
                dialogues.append(line)
        
        return dialogues[:10]  # 限制返回前10个对话
    
    def _get_quality_level(self, score: float) -> str:
        """根据分数获取质量等级"""
        if score >= 9.0:
            return '卓越'
        elif score >= 8.5:
            return '优秀'
        elif score >= 8.0:
            return '良好'
        elif score >= 7.0:
            return '中等'
        elif score >= 6.0:
            return '及格'
        else:
            return '需改进'
    
    def _calculate_final_results(self, optimization_result: Dict[str, Any], chapter_numbers: List[int]) -> Dict[str, Any]:
        """计算最终结果"""
        # 统计成功优化的章节数
        optimized_count = 0
        total_improvements = []
        
        for stage_name, stage_result in optimization_result['stage_results'].items():
            if stage_result.get('success') and 'results' in stage_result:
                results = stage_result['results']
                
                # 统计各阶段的优化章节
                if stage_name == 'content_optimization':
                    optimized_count += len(results.get('optimized_chapters', []))
                    if results.get('improvements_applied'):
                        total_improvements.extend(results['improvements_applied'])
                
                elif stage_name == 'coherence_check':
                    improved_chapters = results.get('improved_chapters', [])
                    if improved_chapters:
                        optimized_count += len(improved_chapters)
                        total_improvements.append('连贯性改进')
                
                elif stage_name == 'dialogue_optimization':
                    if results.get('dialogues_optimized', 0) > 0:
                        total_improvements.append('对话优化')
                
                elif stage_name == 'quality_enhancement':
                    optimized_count += len(results.get('enhanced_chapters', []))
                    if results.get('enhanced_chapters'):
                        total_improvements.append('质量增强')
                
                elif stage_name == 'style_refinement':
                    optimized_count += len(results.get('refined_chapters', []))
                    if results.get('refined_chapters'):
                        total_improvements.append('风格精炼')
                
                elif stage_name == 'multimodal_enrichment':
                    if results.get('enriched_chapters'):
                        total_improvements.append('多模态丰富')
        
        # 计算整体改进
        optimization_result['optimized_chapters'] = min(optimized_count, len(chapter_numbers))
        optimization_result['overall_improvements'] = list(set(total_improvements))  # 去重
        optimization_result['success'] = optimized_count > 0
        optimization_result['end_time'] = datetime.now().isoformat()
        
        # 计算质量改进度
        final_validation = optimization_result['stage_results'].get('final_validation', {})
        if final_validation.get('success') and 'results' in final_validation:
            validation_results = final_validation['results']
            if validation_results.get('overall_assessment'):
                average_quality = validation_results['overall_assessment'].get('average_quality', 0)
                optimization_result['quality_improvement'] = average_quality
        
        return optimization_result
    
    def _generate_optimization_report(self, optimization_result: Dict[str, Any]):
        """生成优化报告"""
        report = {
            'optimization_summary': {
                'total_chapters': optimization_result['total_chapters'],
                'optimized_chapters': optimization_result['optimized_chapters'],
                'success_rate': optimization_result['optimized_chapters'] / optimization_result['total_chapters'],
                'overall_improvements': optimization_result['overall_improvements'],
                'final_quality_score': optimization_result.get('quality_improvement', 0)
            },
            'stage_performance': {},
            'recommendations': [],
            'generated_at': datetime.now().isoformat()
        }
        
        # 分析各阶段表现
        for stage_name, stage_result in optimization_result['stage_results'].items():
            report['stage_performance'][stage_name] = {
                'success': stage_result.get('success', False),
                'message': stage_result.get('message', ''),
                'execution_time': 'N/A'  # 可以添加时间记录
            }
        
        # 生成建议
        if optimization_result['success']:
            if optimization_result.get('quality_improvement', 0) >= 8.5:
                report['recommendations'].append('小说质量已达到优秀水平，可以考虑发布')
            elif optimization_result.get('quality_improvement', 0) >= 7.5:
                report['recommendations'].append('小说质量良好，建议进一步精炼细节')
            else:
                report['recommendations'].append('建议继续使用高级优化功能提升质量')
        else:
            report['recommendations'].append('优化过程中遇到问题，建议检查章节内容和配置')
        
        # 保存报告
        self.storage.save_optimization_report(report)
        
        logger.info(f"优化报告已生成并保存")
    
    def optimize_specific_chapters(self, chapter_numbers: List[int], 
                                 optimization_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """优化指定章节"""
        logger.info(f"🎯 开始优化指定章节: {chapter_numbers}")
        
        if optimization_config is None:
            optimization_config = self._get_default_optimization_config()
        
        # 验证章节存在
        existing_chapters = []
        for ch_num in chapter_numbers:
            chapter_data = self.storage.load_chapter(ch_num)
            if chapter_data:
                existing_chapters.append(ch_num)
            else:
                logger.warning(f"章节 {ch_num} 不存在，跳过")
        
        if not existing_chapters:
            return {
                'success': False,
                'error': '没有找到有效的章节',
                'target_chapters': chapter_numbers
            }
        
        # 执行优化流水线（仅针对指定章节）
        optimization_result = {
            'success': False,
            'target_chapters': existing_chapters,
            'optimized_chapters': 0,
            'stage_results': {},
            'overall_improvements': [],
            'config': optimization_config
        }
        
        try:
            # 执行关键优化阶段
            key_stages = ['initial_analysis', 'content_optimization', 'coherence_check', 
                         'dialogue_optimization', 'quality_enhancement', 'style_refinement', 
                         'final_validation']
            
            for stage in key_stages:
                if stage in self.pipeline_stages:
                    logger.info(f"📝 对指定章节执行: {stage}")
                    stage_result = self._execute_stage(stage, existing_chapters, optimization_config)
                    optimization_result['stage_results'][stage] = stage_result
            
            # 计算最终结果
            optimization_result = self._calculate_final_results(optimization_result, existing_chapters)
            
            logger.info(f"✅ 指定章节优化完成")
            return optimization_result
            
        except Exception as e:
            logger.error(f"指定章节优化失败: {e}")
            optimization_result['error'] = str(e)
            return optimization_result
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """获取优化系统状态"""
        all_chapters = self.storage.get_all_chapters()
        
        status = {
            'system_ready': True,
            'total_chapters': len(all_chapters),
            'optimized_chapters': 0,
            'available_engines': [],
            'recent_optimizations': [],
            'system_health': 'healthy'
        }
        
        # 统计已优化的章节
        for chapter in all_chapters:
            optimization_flags = [
                chapter.get('content_optimized', False),
                chapter.get('coherence_improved', False),
                chapter.get('dialogue_optimized', False),
                chapter.get('quality_enhanced', False),
                chapter.get('style_refined', False)
            ]
            
            if any(optimization_flags):
                status['optimized_chapters'] += 1
        
        # 检查可用引擎
        engines = [
            'context_engine', 'premium_engine', 'learning_engine',
            'reflection_engine', 'multimodal_generator', 'quality_analyzer',
            'text_humanizer', 'style_optimizer', 'dialogue_engine'
        ]
        
        for engine_name in engines:
            if hasattr(self, engine_name):
                status['available_engines'].append(engine_name)
        
        # 计算优化率
        if status['total_chapters'] > 0:
            status['optimization_rate'] = status['optimized_chapters'] / status['total_chapters']
        else:
            status['optimization_rate'] = 0
        
        return status

class OptimizationReportGenerator:
    """优化报告生成器"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
    
    def generate_comprehensive_report(self, optimization_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成综合优化报告"""
        report = {
            'executive_summary': self._generate_executive_summary(optimization_result),
            'detailed_analysis': self._generate_detailed_analysis(optimization_result),
            'performance_metrics': self._generate_performance_metrics(optimization_result),
            'recommendations': self._generate_recommendations(optimization_result),
            'technical_details': self._generate_technical_details(optimization_result),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _generate_executive_summary(self, optimization_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成执行摘要"""
        return {
            'optimization_success': optimization_result.get('success', False),
            'total_chapters_processed': optimization_result.get('total_chapters', 0),
            'chapters_improved': optimization_result.get('optimized_chapters', 0),
            'key_improvements': optimization_result.get('overall_improvements', []),
            'final_quality_score': optimization_result.get('quality_improvement', 0),
            'optimization_rate': (optimization_result.get('optimized_chapters', 0) / 
                                 max(optimization_result.get('total_chapters', 1), 1))
        }
    
    def _generate_detailed_analysis(self, optimization_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成详细分析"""
        analysis = {
            'stage_by_stage_results': {},
            'quality_improvements': {},
            'problem_areas_addressed': [],
            'remaining_issues': []
        }
        
        # 分析各阶段结果
        for stage_name, stage_result in optimization_result.get('stage_results', {}).items():
            analysis['stage_by_stage_results'][stage_name] = {
                'status': 'success' if stage_result.get('success') else 'failed',
                'summary': stage_result.get('message', ''),
                'impact': self._assess_stage_impact(stage_name, stage_result)
            }
        
        return analysis
    
    def _generate_performance_metrics(self, optimization_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成性能指标"""
        return {
            'execution_time': self._calculate_execution_time(optimization_result),
            'success_rates_by_stage': self._calculate_stage_success_rates(optimization_result),
            'quality_improvement_metrics': self._calculate_quality_metrics(optimization_result),
            'efficiency_score': self._calculate_efficiency_score(optimization_result)
        }
    
    def _generate_recommendations(self, optimization_result: Dict[str, Any]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        quality_score = optimization_result.get('quality_improvement', 0)
        
        if quality_score >= 9.0:
            recommendations.append("🎉 恭喜！小说质量已达到卓越水平，可以考虑出版发布")
        elif quality_score >= 8.5:
            recommendations.append("👏 小说质量优秀，建议进行最后的细节打磨")
        elif quality_score >= 8.0:
            recommendations.append("📈 小说质量良好，建议继续优化以达到更高水平")
        elif quality_score >= 7.0:
            recommendations.append("⚡ 建议使用高级优化功能进一步提升质量")
        else:
            recommendations.append("🔧 建议重新运行优化流程，重点关注内容质量和连贯性")
        
        # 根据具体问题给出建议
        stage_results = optimization_result.get('stage_results', {})
        
        if not stage_results.get('coherence_check', {}).get('success'):
            recommendations.append("🔗 建议重点关注章节间的连贯性问题")
        
        if not stage_results.get('dialogue_optimization', {}).get('success'):
            recommendations.append("💬 建议加强对话的自然度和个性化表达")
        
        return recommendations
    
    def _generate_technical_details(self, optimization_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成技术细节"""
        return {
            'optimization_config': optimization_result.get('config', {}),
            'pipeline_stages_executed': list(optimization_result.get('stage_results', {}).keys()),
            'engines_utilized': [
                'context_coherence_engine',
                'premium_content_engine', 
                'dynamic_learning_engine',
                'quality_analyzer',
                'text_humanizer',
                'style_optimizer'
            ],
            'processing_statistics': {
                'start_time': optimization_result.get('start_time'),
                'end_time': optimization_result.get('end_time'),
                'total_stages': len(optimization_result.get('stage_results', {}))
            }
        }
    
    def _assess_stage_impact(self, stage_name: str, stage_result: Dict[str, Any]) -> str:
        """评估阶段影响"""
        if not stage_result.get('success'):
            return 'minimal'
        
        # 根据阶段类型和结果评估影响
        results = stage_result.get('results', {})
        
        if stage_name == 'content_optimization':
            optimized_count = len(results.get('optimized_chapters', []))
            return 'high' if optimized_count > 2 else 'medium' if optimized_count > 0 else 'low'
        
        elif stage_name == 'quality_enhancement':
            avg_improvement = results.get('average_improvement', 0)
            return 'high' if avg_improvement > 1.0 else 'medium' if avg_improvement > 0.5 else 'low'
        
        elif stage_name == 'coherence_check':
            coherence_score = results.get('overall_coherence_score', 0)
            return 'high' if coherence_score >= 8.0 else 'medium' if coherence_score >= 7.0 else 'low'
        
        return 'medium'  # 默认
    
    def _calculate_execution_time(self, optimization_result: Dict[str, Any]) -> Dict[str, Any]:
        """计算执行时间"""
        start_time = optimization_result.get('start_time')
        end_time = optimization_result.get('end_time')
        
        if start_time and end_time:
            try:
                from datetime import datetime
                start_dt = datetime.fromisoformat(start_time)
                end_dt = datetime.fromisoformat(end_time)
                duration = (end_dt - start_dt).total_seconds()
                
                return {
                    'total_seconds': duration,
                    'total_minutes': duration / 60,
                    'formatted_duration': f"{duration//60:.0f}分{duration%60:.0f}秒"
                }
            except:
                pass
        
        return {'total_seconds': 0, 'total_minutes': 0, 'formatted_duration': '未知'}
    
    def _calculate_stage_success_rates(self, optimization_result: Dict[str, Any]) -> Dict[str, float]:
        """计算各阶段成功率"""
        success_rates = {}
        
        for stage_name, stage_result in optimization_result.get('stage_results', {}).items():
            success_rates[stage_name] = 1.0 if stage_result.get('success') else 0.0
        
        return success_rates
    
    def _calculate_quality_metrics(self, optimization_result: Dict[str, Any]) -> Dict[str, Any]:
        """计算质量指标"""
        return {
            'final_average_quality': optimization_result.get('quality_improvement', 0),
            'quality_threshold_met': optimization_result.get('quality_improvement', 0) >= 
                                   optimization_result.get('config', {}).get('target_quality_score', 8.5),
            'improvement_areas': optimization_result.get('overall_improvements', [])
        }
    
    def _calculate_efficiency_score(self, optimization_result: Dict[str, Any]) -> float:
        """计算效率评分"""
        # 基于成功率、质量提升和处理时间计算效率评分
        success_rate = (optimization_result.get('optimized_chapters', 0) / 
                       max(optimization_result.get('total_chapters', 1), 1))
        
        quality_factor = min(optimization_result.get('quality_improvement', 0) / 10.0, 1.0)
        
        # 简化的效率计算
        efficiency = (success_rate * 0.6 + quality_factor * 0.4) * 10
        
        return min(efficiency, 10.0)
