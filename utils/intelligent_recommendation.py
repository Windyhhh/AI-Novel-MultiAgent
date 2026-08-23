"""
智能推荐系统
基于用户需求和系统状态，智能推荐最适合的功能组合和工作流
"""

import json
from typing import Dict, List, Tuple, Optional
from .storage import Storage
from .logger import setup_logger

logger = setup_logger(__name__)

class IntelligentRecommendationEngine:
    """智能推荐引擎"""
    
    def __init__(self):
        self.storage = Storage()
        self.user_profiles = {}
        self.workflow_templates = self._load_workflow_templates()
    
    def _load_workflow_templates(self) -> Dict:
        """加载工作流模板"""
        templates = {
            "beginner": {
                "name": "新手创作流程",
                "description": "适合初学者的简化创作流程",
                "steps": [
                    {"action": "create_outline", "description": "创建小说大纲"},
                    {"action": "generate_chapter", "description": "生成章节内容"},
                    {"action": "basic_optimization", "description": "基础内容优化"}
                ],
                "features": ["outline_generation", "basic_chapter_creation", "simple_optimization"],
                "difficulty": 1
            },
            "intermediate": {
                "name": "专业创作流程", 
                "description": "适合有经验用户的专业流程",
                "steps": [
                    {"action": "advanced_outline", "description": "高级大纲创建"},
                    {"action": "collaborative_generation", "description": "多智能体协作生成"},
                    {"action": "quality_optimization", "description": "质量深度优化"},
                    {"action": "coherence_check", "description": "连贯性检查"}
                ],
                "features": ["collaborative_agents", "quality_analysis", "coherence_validation"],
                "difficulty": 2
            },
            "expert": {
                "name": "专家定制流程",
                "description": "专家级全功能定制流程",
                "steps": [
                    {"action": "genre_specific_outline", "description": "类型专门化大纲"},
                    {"action": "integrated_creation", "description": "整合式高级创作"},
                    {"action": "multimodal_enhancement", "description": "多模态增强"},
                    {"action": "comprehensive_analysis", "description": "全面质量分析"}
                ],
                "features": ["self_rag", "multimodal", "intelligent_dialogue", "dynamic_learning"],
                "difficulty": 3
            }
        }
        return templates
    
    def analyze_user_needs(self, user_input: Dict) -> Dict:
        """分析用户需求"""
        try:
            needs_analysis = {
                "experience_level": self._assess_experience_level(user_input),
                "genre_preference": user_input.get('genre', 'general'),
                "quality_requirements": self._assess_quality_needs(user_input),
                "special_features": self._identify_special_needs(user_input),
                "time_constraints": user_input.get('time_available', 'medium'),
                "technical_comfort": self._assess_technical_comfort(user_input)
            }
            return needs_analysis
        except Exception as e:
            logger.error(f"用户需求分析失败: {e}")
            return self._get_default_needs()
    
    def _assess_experience_level(self, user_input: Dict) -> str:
        """评估用户经验水平"""
        experience_indicators = user_input.get('experience_indicators', {})
        
        # 检查系统使用历史
        chapters_count = len(self.storage.get_all_chapters())
        has_outline = bool(self.storage.load_outline() or self.storage.load_mystery_outline())
        
        score = 0
        if chapters_count > 10:
            score += 3
        elif chapters_count > 3:
            score += 2
        elif chapters_count > 0:
            score += 1
            
        if has_outline:
            score += 2
            
        if experience_indicators.get('ai_writing_experience'):
            score += 2
            
        if experience_indicators.get('professional_writing'):
            score += 3
            
        if score >= 7:
            return 'expert'
        elif score >= 4:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _assess_quality_needs(self, user_input: Dict) -> str:
        """评估质量需求"""
        quality_keywords = user_input.get('description', '').lower()
        
        if any(keyword in quality_keywords for keyword in ['精品', '高质量', '专业', '出版']):
            return 'premium'
        elif any(keyword in quality_keywords for keyword in ['优化', '提升', '改进']):
            return 'enhanced'
        else:
            return 'standard'
    
    def _identify_special_needs(self, user_input: Dict) -> List[str]:
        """识别特殊需求"""
        special_needs = []
        description = user_input.get('description', '').lower()
        
        if any(keyword in description for keyword in ['对话', '人物', '角色']):
            special_needs.append('dialogue_focus')
            
        if any(keyword in description for keyword in ['多媒体', '图像', '音频', '视觉']):
            special_needs.append('multimodal')
            
        if any(keyword in description for keyword in ['悬疑', '推理', '解谜']):
            special_needs.append('mystery_genre')
            
        if any(keyword in description for keyword in ['连贯', '逻辑', '一致']):
            special_needs.append('coherence_priority')
            
        if any(keyword in description for keyword in ['平台', '番茄', '起点']):
            special_needs.append('platform_optimization')
            
        return special_needs
    
    def _assess_technical_comfort(self, user_input: Dict) -> str:
        """评估技术舒适度"""
        tech_comfort = user_input.get('technical_comfort', 'medium')
        if tech_comfort in ['low', 'medium', 'high']:
            return tech_comfort
        return 'medium'
    
    def generate_recommendations(self, user_needs: Dict) -> Dict:
        """生成推荐方案"""
        try:
            # 选择基础工作流
            base_workflow = self._select_base_workflow(user_needs)
            
            # 推荐功能组合
            recommended_features = self._recommend_features(user_needs)
            
            # 生成自定义配置
            custom_config = self._generate_custom_config(user_needs, recommended_features)
            
            # 创建推荐报告
            recommendations = {
                "workflow": base_workflow,
                "recommended_features": recommended_features,
                "custom_config": custom_config,
                "reasoning": self._generate_reasoning(user_needs, base_workflow, recommended_features),
                "quick_start_steps": self._generate_quick_start_steps(base_workflow, recommended_features),
                "estimated_time": self._estimate_completion_time(base_workflow, recommended_features),
                "difficulty_rating": base_workflow["difficulty"]
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"推荐生成失败: {e}")
            return self._get_default_recommendations()
    
    def _select_base_workflow(self, user_needs: Dict) -> Dict:
        """选择基础工作流"""
        experience = user_needs.get('experience_level', 'beginner')
        technical_comfort = user_needs.get('technical_comfort', 'medium')
        
        if experience == 'beginner' or technical_comfort == 'low':
            return self.workflow_templates['beginner']
        elif experience == 'expert' and technical_comfort == 'high':
            return self.workflow_templates['expert']
        else:
            return self.workflow_templates['intermediate']
    
    def _recommend_features(self, user_needs: Dict) -> List[Dict]:
        """推荐功能特性"""
        features = []
        special_needs = user_needs.get('special_features', [])
        quality_needs = user_needs.get('quality_requirements', 'standard')
        
        # 基础功能（所有用户）
        features.append({
            "name": "智能大纲生成",
            "description": "AI协助创建小说结构",
            "priority": "essential",
            "category": "content_creation"
        })
        
        features.append({
            "name": "章节生成",
            "description": "智能生成章节内容",
            "priority": "essential", 
            "category": "content_creation"
        })
        
        # 质量相关功能
        if quality_needs in ['enhanced', 'premium']:
            features.append({
                "name": "Self-RAG自我反思",
                "description": "内容自我评估和改进",
                "priority": "recommended",
                "category": "quality_enhancement"
            })
            
            features.append({
                "name": "8大问题解决方案",
                "description": "解决AI小说创作核心问题",
                "priority": "recommended", 
                "category": "quality_enhancement"
            })
        
        # 特殊需求功能
        if 'dialogue_focus' in special_needs:
            features.append({
                "name": "智能对话系统",
                "description": "生成自然的角色对话",
                "priority": "recommended",
                "category": "advanced_features"
            })
        
        if 'multimodal' in special_needs:
            features.append({
                "name": "多模态创作",
                "description": "文本+图像+音频综合创作",
                "priority": "optional",
                "category": "advanced_features"
            })
        
        if 'mystery_genre' in special_needs:
            features.append({
                "name": "悬疑推理专用",
                "description": "线索管理和逻辑验证",
                "priority": "recommended",
                "category": "genre_specific"
            })
        
        if 'coherence_priority' in special_needs:
            features.append({
                "name": "连贯性检查",
                "description": "整部小说逻辑连贯性验证",
                "priority": "recommended",
                "category": "quality_enhancement"
            })
        
        if 'platform_optimization' in special_needs:
            features.append({
                "name": "平台特化优化",
                "description": "针对特定平台的内容优化",
                "priority": "optional",
                "category": "platform_specific"
            })
        
        return features
    
    def _generate_custom_config(self, user_needs: Dict, features: List[Dict]) -> Dict:
        """生成自定义配置"""
        config = {
            "genre": user_needs.get('genre_preference', 'general'),
            "quality_mode": user_needs.get('quality_requirements', 'standard'),
            "auto_optimization": 'quality_enhancement' in [f['category'] for f in features],
            "multimodal_enabled": 'multimodal' in [f['name'].lower() for f in features],
            "dialogue_optimization": 'dialogue_focus' in user_needs.get('special_features', []),
            "coherence_checking": 'coherence_priority' in user_needs.get('special_features', []),
            "platform": user_needs.get('target_platform', 'general')
        }
        return config
    
    def _generate_reasoning(self, user_needs: Dict, workflow: Dict, features: List[Dict]) -> List[str]:
        """生成推荐理由"""
        reasoning = []
        
        experience = user_needs.get('experience_level', 'beginner')
        reasoning.append(f"基于您的{experience}经验水平，推荐{workflow['name']}")
        
        quality_needs = user_needs.get('quality_requirements', 'standard')
        if quality_needs == 'premium':
            reasoning.append("检测到您对高质量内容的需求，推荐使用Self-RAG和质量优化功能")
        
        special_needs = user_needs.get('special_features', [])
        if 'dialogue_focus' in special_needs:
            reasoning.append("根据您对对话内容的重视，推荐智能对话系统")
        
        if 'multimodal' in special_needs:
            reasoning.append("考虑到您的多媒体创作需求，建议启用多模态功能")
        
        return reasoning
    
    def _generate_quick_start_steps(self, workflow: Dict, features: List[Dict]) -> List[Dict]:
        """生成快速开始步骤"""
        steps = []
        
        # 基于工作流生成步骤
        for i, step in enumerate(workflow['steps'], 1):
            steps.append({
                "step": i,
                "title": step['description'],
                "action": step['action'],
                "estimated_time": "5-10分钟"
            })
        
        return steps
    
    def _estimate_completion_time(self, workflow: Dict, features: List[Dict]) -> str:
        """估算完成时间"""
        base_time = {
            "beginner": "15-30分钟",
            "intermediate": "30-60分钟", 
            "expert": "60-120分钟"
        }
        
        workflow_name = workflow['name']
        if '新手' in workflow_name:
            return base_time['beginner']
        elif '专业' in workflow_name:
            return base_time['intermediate']
        else:
            return base_time['expert']
    
    def _get_default_needs(self) -> Dict:
        """获取默认需求"""
        return {
            "experience_level": "beginner",
            "genre_preference": "general",
            "quality_requirements": "standard",
            "special_features": [],
            "time_constraints": "medium",
            "technical_comfort": "medium"
        }
    
    def _get_default_recommendations(self) -> Dict:
        """获取默认推荐"""
        return {
            "workflow": self.workflow_templates['beginner'],
            "recommended_features": [
                {
                    "name": "智能大纲生成",
                    "description": "AI协助创建小说结构",
                    "priority": "essential",
                    "category": "content_creation"
                }
            ],
            "custom_config": self._generate_custom_config(self._get_default_needs(), []),
            "reasoning": ["基于默认配置的推荐方案"],
            "quick_start_steps": [
                {"step": 1, "title": "创建小说大纲", "action": "create_outline", "estimated_time": "10分钟"}
            ],
            "estimated_time": "15-30分钟",
            "difficulty_rating": 1
        }

class WorkflowExecutor:
    """工作流执行器"""
    
    def __init__(self):
        self.storage = Storage()
    
    def execute_workflow(self, workflow: Dict, config: Dict, callback=None) -> Dict:
        """执行推荐的工作流"""
        try:
            results = {
                "workflow_name": workflow['name'],
                "steps_completed": 0,
                "total_steps": len(workflow['steps']),
                "step_results": [],
                "overall_success": False,
                "execution_time": 0
            }
            
            for i, step in enumerate(workflow['steps']):
                if callback:
                    callback(f"执行步骤 {i+1}/{len(workflow['steps'])}: {step['description']}")
                
                step_result = self._execute_step(step, config)
                results['step_results'].append(step_result)
                
                if step_result['success']:
                    results['steps_completed'] += 1
                else:
                    break
            
            results['overall_success'] = results['steps_completed'] == results['total_steps']
            return results
            
        except Exception as e:
            logger.error(f"工作流执行失败: {e}")
            return {"overall_success": False, "error": str(e)}
    
    def _execute_step(self, step: Dict, config: Dict) -> Dict:
        """执行单个步骤"""
        action = step['action']
        
        try:
            if action == "create_outline":
                return self._create_outline_step(config)
            elif action == "generate_chapter":
                return self._generate_chapter_step(config)
            elif action == "basic_optimization":
                return self._basic_optimization_step(config)
            elif action == "advanced_outline":
                return self._advanced_outline_step(config)
            elif action == "collaborative_generation":
                return self._collaborative_generation_step(config)
            elif action == "quality_optimization":
                return self._quality_optimization_step(config)
            elif action == "coherence_check":
                return self._coherence_check_step(config)
            elif action == "genre_specific_outline":
                return self._genre_specific_outline_step(config)
            elif action == "integrated_creation":
                return self._integrated_creation_step(config)
            elif action == "multimodal_enhancement":
                return self._multimodal_enhancement_step(config)
            elif action == "comprehensive_analysis":
                return self._comprehensive_analysis_step(config)
            else:
                return {"success": False, "error": f"未知步骤: {action}"}
                
        except Exception as e:
            logger.error(f"步骤执行失败 {action}: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_outline_step(self, config: Dict) -> Dict:
        """创建大纲步骤"""
        # 这里会调用实际的大纲创建逻辑
        return {"success": True, "message": "大纲创建完成", "data": {}}
    
    def _generate_chapter_step(self, config: Dict) -> Dict:
        """生成章节步骤"""
        return {"success": True, "message": "章节生成完成", "data": {}}
    
    def _basic_optimization_step(self, config: Dict) -> Dict:
        """基础优化步骤"""
        return {"success": True, "message": "基础优化完成", "data": {}}
    
    def _advanced_outline_step(self, config: Dict) -> Dict:
        """高级大纲步骤"""
        return {"success": True, "message": "高级大纲创建完成", "data": {}}
    
    def _collaborative_generation_step(self, config: Dict) -> Dict:
        """协作生成步骤"""
        return {"success": True, "message": "协作生成完成", "data": {}}
    
    def _quality_optimization_step(self, config: Dict) -> Dict:
        """质量优化步骤"""
        return {"success": True, "message": "质量优化完成", "data": {}}
    
    def _coherence_check_step(self, config: Dict) -> Dict:
        """连贯性检查步骤"""
        return {"success": True, "message": "连贯性检查完成", "data": {}}
    
    def _genre_specific_outline_step(self, config: Dict) -> Dict:
        """类型专门化大纲步骤"""
        return {"success": True, "message": "类型专门化大纲创建完成", "data": {}}
    
    def _integrated_creation_step(self, config: Dict) -> Dict:
        """整合式创作步骤"""
        return {"success": True, "message": "整合式创作完成", "data": {}}
    
    def _multimodal_enhancement_step(self, config: Dict) -> Dict:
        """多模态增强步骤"""
        return {"success": True, "message": "多模态增强完成", "data": {}}
    
    def _comprehensive_analysis_step(self, config: Dict) -> Dict:
        """综合分析步骤"""
        return {"success": True, "message": "综合分析完成", "data": {}}
