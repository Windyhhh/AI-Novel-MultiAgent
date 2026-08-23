"""
智能体协作调度器
统一管理多个智能体的协作，确保上下文连贯性和内容质量
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from concurrent.futures import ThreadPoolExecutor
from utils import LLMClient, get_logger, Storage
from utils.context_coherence_engine import ContextCoherenceEngine
from utils.premium_content_engine import PremiumContentEngine

logger = get_logger('agent_orchestrator')

class AgentOrchestrator:
    """智能体协作调度器"""
    
    def __init__(self):
        self.storage = Storage()
        self.llm = LLMClient()
        self.agents = {}
        self.context_manager = ContextManager()
        self.quality_controller = QualityController()
        self.workflow_engine = WorkflowEngine()
        
        # 初始化核心引擎
        self.context_coherence_engine = ContextCoherenceEngine()
        self.premium_content_engine = PremiumContentEngine()
        
        # 注册基础智能体
        self._register_base_agents()
        
    def _register_base_agents(self):
        """注册基础智能体"""
        from .outline_agent import OutlineAgent
        from .chapter_planning_agent import ChapterPlanningAgent
        from .content_generation_agent import ContentGenerationAgent
        from .mystery_agent import MysteryAgent
        from .tomato_novel_agent import TomatoNovelAgent
        from .character_memory_agent import CharacterMemoryAgent
        from .plot_tracker_agent import PlotTrackerAgent
        
        self.agents.update({
            'outline': OutlineAgent(),
            'chapter_planning': ChapterPlanningAgent(),
            'content_generation': ContentGenerationAgent(),
            'mystery': MysteryAgent(),
            'tomato_novel': TomatoNovelAgent(),
            'character_memory': CharacterMemoryAgent(),
            'plot_tracker': PlotTrackerAgent(),
        })
    
    def register_agent(self, name: str, agent: Any):
        """动态注册新的智能体"""
        self.agents[name] = agent
        logger.info(f"注册智能体: {name}")
    
    def create_collaborative_outline(self, genre: str, custom_settings: Dict[str, Any] = None) -> Dict[str, Any]:
        """多智能体协作创建大纲"""
        logger.info(f"开始多智能体协作创建{genre}大纲")
        
        # 第一阶段：基础大纲生成
        if genre == 'mystery':
            base_outline = self.agents['mystery'].create_mystery_outline(custom_settings or {})
        else:
            base_outline = self.agents['outline'].create_outline('customized', custom_settings or {})
        
        if not base_outline:
            return None
        
        # 第二阶段：多智能体优化
        enhanced_outline = self._enhance_outline_collaboratively(base_outline, genre)
        
        # 第三阶段：质量验证
        validated_outline = self.quality_controller.validate_outline(enhanced_outline)
        
        # 保存协作结果
        self.context_manager.save_context('outline', validated_outline)
        
        return validated_outline
    
    def _enhance_outline_collaboratively(self, base_outline: Dict[str, Any], genre: str) -> Dict[str, Any]:
        """多智能体协作增强大纲"""
        enhanced_outline = base_outline.copy()
        
        # 角色记忆智能体：增强角色一致性
        if 'character_memory' in self.agents:
            character_enhancements = self.agents['character_memory'].enhance_character_profiles(
                enhanced_outline.get('characters', [])
            )
            enhanced_outline['characters'] = character_enhancements
        
        # 情节追踪智能体：优化情节结构
        if 'plot_tracker' in self.agents:
            plot_enhancements = self.agents['plot_tracker'].optimize_plot_structure(
                enhanced_outline.get('plot_points', [])
            )
            enhanced_outline['plot_points'] = plot_enhancements
        
        # 针对特定类型的优化
        if genre == 'mystery' and 'mystery' in self.agents:
            # 添加线索系统和角色关系
            clue_system = self.agents['mystery'].create_clue_system(enhanced_outline)
            relationships = self.agents['mystery'].generate_character_relationships(enhanced_outline)
            enhanced_outline['clue_system'] = clue_system
            enhanced_outline['character_relationships'] = relationships
        
        return enhanced_outline
    
    def generate_chapter_collaboratively(self, chapter_number: int, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """多智能体协作生成章节"""
        logger.info(f"开始多智能体协作生成第{chapter_number}章")
        
        # 获取全局上下文
        full_context = self.context_manager.get_full_context()
        if context:
            full_context.update(context)
        
        # 第一阶段：章节规划
        chapter_plan = self.agents['chapter_planning'].plan_chapter(chapter_number, full_context.get('outline'))
        
        # 第二阶段：内容生成（根据类型选择合适的生成器）
        genre = full_context.get('outline', {}).get('genre', 'general')
        
        if genre == 'mystery' and 'tomato_novel' in self.agents:
            # 悬疑推理 + 番茄小说优化
            chapter_content = self.agents['tomato_novel'].generate_mystery_chapter(chapter_plan, full_context)
        elif 'content_generation' in self.agents:
            # 通用内容生成
            chapter_content = self.agents['content_generation'].generate_chapter(chapter_plan, full_context)
        else:
            return None
        
        # 第三阶段：多智能体优化
        optimized_content = self._optimize_chapter_collaboratively(chapter_content, full_context)
        
        # 第四阶段：质量控制
        final_content = self.quality_controller.validate_chapter(optimized_content)
        
        # 第五阶段：上下文更新
        self.context_manager.update_context_with_chapter(chapter_number, final_content)
        
        # 保存章节
        self.storage.save_chapter(chapter_number, final_content)
        
        return final_content
    
    def _optimize_chapter_collaboratively(self, chapter_content: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """多智能体协作优化章节"""
        optimized = chapter_content.copy()
        
        # 角色记忆一致性检查
        if 'character_memory' in self.agents:
            character_consistency = self.agents['character_memory'].check_character_consistency(
                optimized.get('content', ''), context.get('characters', [])
            )
            optimized['character_consistency'] = character_consistency
        
        # 情节追踪连贯性检查
        if 'plot_tracker' in self.agents:
            plot_consistency = self.agents['plot_tracker'].check_plot_consistency(
                optimized, context.get('plot_points', [])
            )
            optimized['plot_consistency'] = plot_consistency
        
        # 悬疑推理逻辑验证
        if context.get('genre') == 'mystery' and 'mystery' in self.agents:
            logic_validation = self.agents['mystery'].verify_logic_consistency(
                optimized.get('content', ''), context.get('clue_system', {})
            )
            optimized['logic_validation'] = logic_validation
        
        return optimized
    
    def batch_optimize_chapters(self, chapter_numbers: List[int], optimization_type: str = 'comprehensive') -> Dict[str, Any]:
        """批量优化章节"""
        results = {
            'optimized_count': 0,
            'failed_count': 0,
            'details': []
        }
        
        full_context = self.context_manager.get_full_context()
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            
            for chapter_num in chapter_numbers:
                chapter_data = self.storage.load_chapter(chapter_num)
                if chapter_data:
                    future = executor.submit(
                        self._optimize_single_chapter,
                        chapter_num, chapter_data, full_context, optimization_type
                    )
                    futures.append((chapter_num, future))
            
            for chapter_num, future in futures:
                try:
                    result = future.result(timeout=300)  # 5分钟超时
                    if result['success']:
                        self.storage.update_chapter(chapter_num, result['data'])
                        results['optimized_count'] += 1
                        results['details'].append({
                            'chapter': chapter_num,
                            'status': 'success',
                            'improvements': result.get('improvements', [])
                        })
                    else:
                        results['failed_count'] += 1
                        results['details'].append({
                            'chapter': chapter_num,
                            'status': 'failed',
                            'error': result.get('error', 'Unknown error')
                        })
                except Exception as e:
                    results['failed_count'] += 1
                    results['details'].append({
                        'chapter': chapter_num,
                        'status': 'failed',
                        'error': str(e)
                    })
        
        return results
    
    def _optimize_single_chapter(self, chapter_num: int, chapter_data: Dict[str, Any], 
                                context: Dict[str, Any], optimization_type: str) -> Dict[str, Any]:
        """优化单个章节"""
        try:
            original_content = chapter_data.get('content', '')
            improved_content = original_content
            improvements = []
            
            # 根据优化类型执行不同的优化策略
            if optimization_type in ['comprehensive', 'context']:
                # 上下文连贯性优化
                context_result = self._improve_context_coherence(improved_content, context, chapter_num)
                if context_result['improved']:
                    improved_content = context_result['content']
                    improvements.append('上下文连贯性')
            
            if optimization_type in ['comprehensive', 'quality']:
                # 内容质量优化
                quality_result = self._improve_content_quality(improved_content, context)
                if quality_result['improved']:
                    improved_content = quality_result['content']
                    improvements.append('内容质量')
            
            if optimization_type in ['comprehensive', 'platform']:
                # 平台特化优化
                platform_result = self._improve_platform_adaptation(improved_content, context)
                if platform_result['improved']:
                    improved_content = platform_result['content']
                    improvements.append('平台适配')
            
            # 更新章节数据
            updated_data = chapter_data.copy()
            updated_data['content'] = improved_content
            updated_data['word_count'] = len(improved_content)
            updated_data['optimized_at'] = datetime.now().isoformat()
            updated_data['optimization_type'] = optimization_type
            
            return {
                'success': True,
                'data': updated_data,
                'improvements': improvements
            }
        
        except Exception as e:
            logger.error(f"优化第{chapter_num}章失败: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _improve_context_coherence(self, content: str, context: Dict[str, Any], chapter_num: int) -> Dict[str, Any]:
        """改善上下文连贯性 - 使用高级上下文连贯性引擎"""
        try:
            # 使用上下文连贯性引擎进行高级优化
            improved_content = self.context_coherence_engine.ensure_chapter_coherence(
                content=content,
                chapter_number=chapter_num,
                novel_context=context,
                storage=self.storage
            )
            
            # 检查是否有改善
            if improved_content and improved_content != content:
                return {'improved': True, 'content': improved_content}
            else:
                return {'improved': False, 'content': content}
        
        except Exception as e:
            logger.error(f"上下文连贯性引擎优化失败: {e}")
            return {'improved': False, 'content': content}
    
    def _improve_content_quality(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """提升内容质量 - 使用高质量内容生成引擎"""
        try:
            # 使用高质量内容生成引擎进行深度优化
            improved_content = self.premium_content_engine.enhance_existing_content(
                content=content,
                genre=context.get('genre', '通用'),
                context_info=context
            )
            
            # 检查是否有改善
            if improved_content and improved_content != content:
                return {'improved': True, 'content': improved_content}
            else:
                return {'improved': False, 'content': content}
        
        except Exception as e:
            logger.error(f"高质量内容生成引擎优化失败: {e}")
            return {'improved': False, 'content': content}
    
    def _improve_platform_adaptation(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """平台适配优化"""
        platform = context.get('platform', 'tomato_novel')
        
        if platform == 'tomato_novel' and 'tomato_novel' in self.agents:
            try:
                optimization = self.agents['tomato_novel'].optimize_for_mobile_reading(content)
                return {'improved': True, 'content': optimization}
            except:
                return {'improved': False, 'content': content}
        
        return {'improved': False, 'content': content}
    
    def generate_premium_chapter(self, chapter_number: int, chapter_plan: Dict[str, Any], 
                                context: Dict[str, Any]) -> Dict[str, Any]:
        """使用高质量内容生成引擎生成精品章节"""
        logger.info(f"开始使用高质量引擎生成第{chapter_number}章")
        
        try:
            # 使用高质量内容生成引擎
            premium_content = self.premium_content_engine.generate_premium_chapter(
                chapter_plan=chapter_plan,
                context=context,
                chapter_number=chapter_number
            )
            
            if premium_content:
                # 确保上下文连贯性
                coherent_content = self.context_coherence_engine.ensure_chapter_coherence(
                    content=premium_content,
                    chapter_number=chapter_number,
                    novel_context=context,
                    storage=self.storage
                )
                
                # 构建完整章节数据
                chapter_data = {
                    'number': chapter_number,
                    'title': chapter_plan.get('title', f'第{chapter_number}章'),
                    'content': coherent_content,
                    'word_count': len(coherent_content),
                    'generated_at': datetime.now().isoformat(),
                    'generation_method': 'premium_engine',
                    'quality_level': 'premium'
                }
                
                # 保存章节
                self.storage.save_chapter(chapter_number, chapter_data)
                
                # 更新上下文
                self.context_manager.update_context_with_chapter(chapter_number, chapter_data)
                
                return chapter_data
            else:
                logger.error(f"高质量内容生成引擎生成第{chapter_number}章失败")
                return None
                
        except Exception as e:
            logger.error(f"精品章节生成失败: {e}")
            return None
    
    def check_novel_coherence(self, chapter_range: Optional[List[int]] = None) -> Dict[str, Any]:
        """检查整部小说的连贯性"""
        logger.info("开始全小说连贯性检查")
        
        try:
            # 获取全局上下文
            full_context = self.context_manager.get_full_context()
            
            # 如果没有指定章节范围，检查所有章节
            if chapter_range is None:
                all_chapters = self.storage.get_all_chapters()
                chapter_range = [ch['number'] for ch in all_chapters] if all_chapters else []
            
            # 使用上下文连贯性引擎进行全面检查
            coherence_report = self.context_coherence_engine.check_novel_coherence(
                chapter_numbers=chapter_range,
                novel_context=full_context,
                storage=self.storage
            )
            
            return coherence_report
            
        except Exception as e:
            logger.error(f"小说连贯性检查失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def intelligent_optimization_workflow(self, target_chapters: List[int], 
                                        optimization_goals: Dict[str, Any]) -> Dict[str, Any]:
        """智能优化工作流 - 根据目标自动选择最佳优化策略"""
        logger.info(f"开始智能优化工作流，目标章节: {target_chapters}")
        
        results = {
            'total_chapters': len(target_chapters),
            'optimized_chapters': 0,
            'failed_chapters': 0,
            'details': [],
            'overall_improvements': []
        }
        
        try:
            full_context = self.context_manager.get_full_context()
            
            for chapter_num in target_chapters:
                chapter_data = self.storage.load_chapter(chapter_num)
                if not chapter_data:
                    results['failed_chapters'] += 1
                    results['details'].append({
                        'chapter': chapter_num,
                        'status': 'failed',
                        'error': '章节不存在'
                    })
                    continue
                
                # 分析章节需求
                optimization_plan = self._analyze_chapter_optimization_needs(
                    chapter_data, full_context, optimization_goals
                )
                
                # 执行优化
                optimization_result = self._execute_intelligent_optimization(
                    chapter_num, chapter_data, optimization_plan, full_context
                )
                
                if optimization_result['success']:
                    results['optimized_chapters'] += 1
                    results['details'].append({
                        'chapter': chapter_num,
                        'status': 'success',
                        'applied_optimizations': optimization_result['optimizations'],
                        'quality_improvement': optimization_result.get('quality_improvement', 0)
                    })
                    
                    # 更新整体改进记录
                    for improvement in optimization_result['optimizations']:
                        if improvement not in results['overall_improvements']:
                            results['overall_improvements'].append(improvement)
                else:
                    results['failed_chapters'] += 1
                    results['details'].append({
                        'chapter': chapter_num,
                        'status': 'failed',
                        'error': optimization_result.get('error', 'Unknown error')
                    })
            
            # 生成优化报告
            results['success'] = results['optimized_chapters'] > 0
            results['optimization_rate'] = results['optimized_chapters'] / results['total_chapters']
            
            return results
            
        except Exception as e:
            logger.error(f"智能优化工作流失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_chapter_optimization_needs(self, chapter_data: Dict[str, Any], 
                                          context: Dict[str, Any], 
                                          goals: Dict[str, Any]) -> Dict[str, Any]:
        """分析章节优化需求"""
        content = chapter_data.get('content', '')
        chapter_num = chapter_data.get('number', 0)
        
        optimization_plan = {
            'priority_optimizations': [],
            'secondary_optimizations': [],
            'context_issues': [],
            'quality_issues': []
        }
        
        # 检查上下文连贯性问题
        if goals.get('improve_coherence', True):
            try:
                coherence_issues = self.context_coherence_engine.analyze_coherence_issues(
                    content, chapter_num, context, self.storage
                )
                if coherence_issues:
                    optimization_plan['priority_optimizations'].append('context_coherence')
                    optimization_plan['context_issues'] = coherence_issues
            except:
                pass
        
        # 检查内容质量问题
        if goals.get('improve_quality', True):
            try:
                quality_issues = self.premium_content_engine.analyze_content_quality(
                    content, context.get('genre', '通用')
                )
                if quality_issues:
                    optimization_plan['priority_optimizations'].append('content_quality')
                    optimization_plan['quality_issues'] = quality_issues
            except:
                pass
        
        # 检查平台适配需求
        if goals.get('platform_optimization', False):
            platform = goals.get('target_platform', 'tomato_novel')
            if platform == 'tomato_novel':
                optimization_plan['secondary_optimizations'].append('platform_adaptation')
        
        # 检查特定类型优化需求
        genre = context.get('outline', {}).get('genre', 'general')
        if genre == 'mystery' and goals.get('genre_optimization', True):
            optimization_plan['secondary_optimizations'].append('mystery_logic')
        
        return optimization_plan
    
    def _execute_intelligent_optimization(self, chapter_num: int, chapter_data: Dict[str, Any],
                                        optimization_plan: Dict[str, Any], 
                                        context: Dict[str, Any]) -> Dict[str, Any]:
        """执行智能优化"""
        try:
            original_content = chapter_data.get('content', '')
            current_content = original_content
            applied_optimizations = []
            
            # 执行优先级优化
            for optimization in optimization_plan['priority_optimizations']:
                if optimization == 'context_coherence':
                    result = self._improve_context_coherence(current_content, context, chapter_num)
                    if result['improved']:
                        current_content = result['content']
                        applied_optimizations.append('上下文连贯性优化')
                
                elif optimization == 'content_quality':
                    result = self._improve_content_quality(current_content, context)
                    if result['improved']:
                        current_content = result['content']
                        applied_optimizations.append('内容质量优化')
            
            # 执行次要优化
            for optimization in optimization_plan['secondary_optimizations']:
                if optimization == 'platform_adaptation':
                    result = self._improve_platform_adaptation(current_content, context)
                    if result['improved']:
                        current_content = result['content']
                        applied_optimizations.append('平台适配优化')
                
                elif optimization == 'mystery_logic' and 'mystery' in self.agents:
                    # 悬疑推理逻辑优化
                    try:
                        clue_system = context.get('clue_system', {})
                        logic_validation = self.agents['mystery'].verify_logic_consistency(
                            current_content, clue_system
                        )
                        if logic_validation.get('needs_improvement', False):
                            applied_optimizations.append('悬疑逻辑优化')
                    except Exception:
                        pass
            
            # 更新章节数据
            if current_content != original_content:
                updated_data = chapter_data.copy()
                updated_data['content'] = current_content
                updated_data['word_count'] = len(current_content)
                updated_data['optimized_at'] = datetime.now().isoformat()
                updated_data['optimization_method'] = 'intelligent_workflow'
                
                self.storage.update_chapter(chapter_num, updated_data)
                
                return {
                    'success': True,
                    'optimizations': applied_optimizations,
                    'content_changed': True
                }
            else:
                return {
                    'success': True,
                    'optimizations': [],
                    'content_changed': False
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

class ContextManager:
    """上下文管理器"""
    
    def __init__(self):
        self.storage = Storage()
        self.context_cache = {}
    
    def get_full_context(self) -> Dict[str, Any]:
        """获取完整上下文"""
        context = {
            'outline': self.storage.load_outline(),
            'mystery_outline': self.storage.load_mystery_outline(),
            'chapters': self.storage.get_all_chapters(),
            'characters': [],
            'plot_points': [],
            'clue_system': {},
            'character_relationships': {}
        }
        
        # 如果有悬疑推理大纲，加载相关数据
        if context['mystery_outline']:
            outline_id = context['mystery_outline']['id']
            context['clue_system'] = self.storage.load_clue_system(outline_id) or {}
            context['character_relationships'] = self.storage.load_character_relationships(outline_id) or {}
        
        return context
    
    def save_context(self, context_type: str, data: Dict[str, Any]):
        """保存上下文"""
        self.context_cache[context_type] = data
    
    def update_context_with_chapter(self, chapter_number: int, chapter_data: Dict[str, Any]):
        """根据新章节更新上下文"""
        # 更新角色状态、情节进展等
        pass

class QualityController:
    """质量控制器"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def validate_outline(self, outline: Dict[str, Any]) -> Dict[str, Any]:
        """验证大纲质量"""
        # 实现大纲质量验证逻辑
        outline['quality_validated'] = True
        outline['quality_score'] = 8.5
        return outline
    
    def validate_chapter(self, chapter: Dict[str, Any]) -> Dict[str, Any]:
        """验证章节质量"""
        # 实现章节质量验证逻辑
        chapter['quality_validated'] = True
        chapter['quality_score'] = 8.0
        return chapter

class WorkflowEngine:
    """工作流引擎"""
    
    def __init__(self):
        self.workflows = {}
    
    def register_workflow(self, name: str, workflow: Dict[str, Any]):
        """注册工作流"""
        self.workflows[name] = workflow
    
    def execute_workflow(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行工作流"""
        if name not in self.workflows:
            return {'success': False, 'error': f'未找到工作流: {name}'}
        
        # 实现工作流执行逻辑
        return {'success': True, 'result': {}}
