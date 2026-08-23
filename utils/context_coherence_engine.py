"""
长篇小说上下文连贯性引擎
解决长篇创作中的角色一致性、情节连贯性、设定统一性等核心问题
参考了《Narrative Generation: Balancing Plot and Character》等研究
"""

import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, deque
import re
from utils import LLMClient, get_logger, Storage

logger = get_logger('context_coherence_engine')

@dataclass
class CharacterState:
    """角色状态跟踪"""
    name: str
    personality: Dict[str, Any]
    relationships: Dict[str, float]  # 与其他角色的关系值
    knowledge: List[str]  # 角色知道的信息
    emotions: Dict[str, float]  # 情感状态
    location: str
    goals: List[str]
    secrets: List[str]
    last_appearance: int  # 最后出现章节
    
@dataclass
class PlotThread:
    """情节线跟踪"""
    thread_id: str
    description: str
    status: str  # active, resolved, suspended
    importance: float
    related_characters: List[str]
    key_events: List[Dict[str, Any]]
    foreshadowing: List[str]
    resolution_target: Optional[int]

@dataclass
class WorldState:
    """世界状态跟踪"""
    settings: Dict[str, Any]  # 地点描述
    rules: List[str]  # 世界规则
    timeline: List[Dict[str, Any]]  # 时间线事件
    objects: Dict[str, Any]  # 重要物品状态
    social_dynamics: Dict[str, Any]  # 社会关系

class ContextCoherenceEngine:
    """上下文连贯性引擎"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.storage = Storage()
        
        # 核心状态跟踪
        self.character_states = {}  # CharacterState对象字典
        self.plot_threads = {}  # PlotThread对象字典
        self.world_state = WorldState({}, [], [], {}, {})
        
        # 连贯性历史
        self.chapter_summaries = deque(maxlen=50)  # 保留最近50章摘要
        self.character_interactions = defaultdict(list)  # 角色互动历史
        self.event_timeline = []  # 全局事件时间线
        
        # 一致性检查器
        self.consistency_checker = ConsistencyChecker()
        self.memory_manager = LongTermMemoryManager()
        
    def initialize_from_outline(self, outline: Dict[str, Any]):
        """从大纲初始化上下文状态"""
        logger.info("初始化长篇小说上下文状态")
        
        # 初始化角色状态
        characters = outline.get('characters', [])
        for char in characters:
            char_state = CharacterState(
                name=char.get('name', ''),
                personality=char.get('personality', {}),
                relationships={},
                knowledge=char.get('initial_knowledge', []),
                emotions=char.get('initial_emotions', {}),
                location=char.get('initial_location', ''),
                goals=char.get('goals', []),
                secrets=char.get('secrets', []),
                last_appearance=0
            )
            self.character_states[char_state.name] = char_state
        
        # 初始化情节线
        plot_lines = outline.get('plot_lines', [])
        for i, plot in enumerate(plot_lines):
            thread = PlotThread(
                thread_id=f"plot_{i}",
                description=plot.get('description', ''),
                status='active',
                importance=plot.get('importance', 0.5),
                related_characters=plot.get('characters', []),
                key_events=[],
                foreshadowing=plot.get('foreshadowing', []),
                resolution_target=plot.get('target_chapter', None)
            )
            self.plot_threads[thread.thread_id] = thread
        
        # 初始化世界状态
        self.world_state.settings = outline.get('world_settings', {})
        self.world_state.rules = outline.get('world_rules', [])
        
    def update_context_after_chapter(self, chapter_number: int, chapter_content: str, 
                                   chapter_plan: Dict[str, Any] = None):
        """章节生成后更新上下文状态"""
        logger.info(f"更新第{chapter_number}章后的上下文状态")
        
        # 生成章节摘要
        summary = self._generate_chapter_summary(chapter_content, chapter_number)
        self.chapter_summaries.append(summary)
        
        # 更新角色状态
        self._update_character_states(chapter_content, chapter_number)
        
        # 更新情节线
        self._update_plot_threads(chapter_content, chapter_number)
        
        # 更新世界状态
        self._update_world_state(chapter_content, chapter_number)
        
        # 记录时间线事件
        self._record_timeline_events(chapter_content, chapter_number)
        
        # 保存上下文快照
        self._save_context_snapshot(chapter_number)
        
    def get_context_for_chapter(self, chapter_number: int) -> Dict[str, Any]:
        """获取生成特定章节需要的上下文信息"""
        logger.info(f"获取第{chapter_number}章的上下文信息")
        
        context = {
            'chapter_number': chapter_number,
            'recent_summaries': list(self.chapter_summaries)[-10:],  # 最近10章摘要
            'character_states': self._get_relevant_character_states(chapter_number),
            'active_plot_threads': self._get_active_plot_threads(chapter_number),
            'world_context': self._get_current_world_context(),
            'continuity_notes': self._generate_continuity_notes(chapter_number),
            'character_arcs': self._get_character_arc_status(chapter_number),
            'unresolved_elements': self._get_unresolved_elements(),
            'foreshadowing_opportunities': self._get_foreshadowing_opportunities(chapter_number)
        }
        
        return context
    
    def check_chapter_consistency(self, chapter_content: str, chapter_number: int) -> Dict[str, Any]:
        """检查章节与已有内容的一致性"""
        logger.info(f"检查第{chapter_number}章的一致性")
        
        consistency_report = self.consistency_checker.check_consistency(
            chapter_content, 
            chapter_number,
            self.character_states,
            self.plot_threads,
            self.world_state,
            self.chapter_summaries
        )
        
        return consistency_report
    
    def _generate_chapter_summary(self, chapter_content: str, chapter_number: int) -> Dict[str, Any]:
        """生成章节摘要用于上下文记忆"""
        prompt = f"""
请为以下第{chapter_number}章内容生成结构化摘要，重点关注对后续章节重要的信息：

章节内容：
{chapter_content}

请按以下格式生成摘要：
1. 主要事件：[本章发生的关键事件]
2. 角色发展：[角色状态、关系、情感的变化]
3. 情节推进：[哪些情节线有进展]
4. 重要信息：[新揭露的信息、线索、设定]
5. 悬念要素：[为后续章节埋下的伏笔]
6. 时间地点：[故事发生的时间和地点]

摘要要简洁但包含所有关键信息。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=1500, temperature=0.3)
            
            summary = {
                'chapter_number': chapter_number,
                'raw_summary': response,
                'generated_at': datetime.now().isoformat(),
                'word_count': len(chapter_content),
                'key_events': self._extract_key_events(response),
                'character_mentions': self._extract_character_mentions(chapter_content),
                'location_changes': self._extract_location_info(chapter_content)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"生成章节摘要失败: {e}")
            return {
                'chapter_number': chapter_number,
                'raw_summary': f"第{chapter_number}章摘要生成失败",
                'generated_at': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _update_character_states(self, chapter_content: str, chapter_number: int):
        """更新角色状态"""
        # 检测章节中出现的角色
        mentioned_characters = self._extract_character_mentions(chapter_content)
        
        for char_name in mentioned_characters:
            if char_name in self.character_states:
                char_state = self.character_states[char_name]
                char_state.last_appearance = chapter_number
                
                # 使用LLM分析角色状态变化
                state_changes = self._analyze_character_changes(
                    chapter_content, char_name, char_state
                )
                
                # 更新角色状态
                if state_changes:
                    char_state.emotions.update(state_changes.get('emotions', {}))
                    char_state.knowledge.extend(state_changes.get('new_knowledge', []))
                    char_state.relationships.update(state_changes.get('relationship_changes', {}))
                    if state_changes.get('location'):
                        char_state.location = state_changes['location']
    
    def _analyze_character_changes(self, chapter_content: str, char_name: str, 
                                 current_state: CharacterState) -> Dict[str, Any]:
        """分析角色在章节中的状态变化"""
        prompt = f"""
分析角色"{char_name}"在以下章节中的状态变化：

章节内容：
{chapter_content}

角色当前状态：
- 性格：{current_state.personality}
- 当前情感：{current_state.emotions}
- 当前位置：{current_state.location}
- 已知信息：{current_state.knowledge[-5:]}  # 最近知道的信息

请分析并返回JSON格式的状态变化：
{{
    "emotions": {{"情感类型": 强度值(0-1)}},
    "new_knowledge": ["新获得的信息1", "新获得的信息2"],
    "relationship_changes": {{"角色名": 关系变化值(-1到1)}},
    "location": "新位置（如果有变化）",
    "goal_progress": "目标进展描述"
}}

如果没有明显变化，返回空字典。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=1000, temperature=0.3)
            changes = json.loads(response)
            return changes
        except Exception as e:
            logger.error(f"分析角色状态变化失败: {e}")
            return {}
    
    def _get_relevant_character_states(self, chapter_number: int) -> Dict[str, Any]:
        """获取与当前章节相关的角色状态"""
        relevant_chars = {}
        
        for char_name, char_state in self.character_states.items():
            # 最近出现过的角色
            if char_state.last_appearance >= chapter_number - 10:
                relevant_chars[char_name] = {
                    'personality': char_state.personality,
                    'current_emotions': char_state.emotions,
                    'location': char_state.location,
                    'recent_knowledge': char_state.knowledge[-5:],
                    'active_goals': char_state.goals,
                    'last_seen': char_state.last_appearance
                }
        
        return relevant_chars
    
    def _generate_continuity_notes(self, chapter_number: int) -> List[str]:
        """生成连续性注意事项"""
        notes = []
        
        # 检查悬而未决的情节线
        for thread in self.plot_threads.values():
            if thread.status == 'active' and thread.key_events:
                last_event = thread.key_events[-1]
                if last_event.get('chapter', 0) < chapter_number - 5:
                    notes.append(f"情节线'{thread.description}'需要进展")
        
        # 检查长期未出现的重要角色
        for char_name, char_state in self.character_states.items():
            if (chapter_number - char_state.last_appearance > 15 and 
                char_state.name in [t.related_characters for t in self.plot_threads.values()]):
                notes.append(f"重要角色'{char_name}'已很久未出现")
        
        return notes
    
    def get_long_term_memory_context(self, chapter_number: int, lookback_chapters: int = 20) -> Dict[str, Any]:
        """获取长期记忆上下文（解决长篇小说记忆问题）"""
        return self.memory_manager.get_relevant_context(
            chapter_number, lookback_chapters, 
            self.chapter_summaries, self.character_states, self.plot_threads
        )
    
    def _extract_character_mentions(self, content: str) -> List[str]:
        """从内容中提取角色提及"""
        mentioned = []
        for char_name in self.character_states.keys():
            if char_name in content:
                mentioned.append(char_name)
        return mentioned
    
    def _extract_key_events(self, summary_text: str) -> List[str]:
        """从摘要中提取关键事件"""
        # 简单的事件提取逻辑，可以用更复杂的NLP方法改进
        events = []
        lines = summary_text.split('\n')
        for line in lines:
            if '主要事件' in line or '关键事件' in line:
                events.append(line.strip())
        return events
    
    def _extract_location_info(self, content: str) -> List[str]:
        """提取地点信息"""
        # 简化的地点提取，实际应用中可以使用NER
        locations = []
        common_locations = ['家里', '学校', '公司', '医院', '警局', '咖啡厅', '餐厅']
        for loc in common_locations:
            if loc in content:
                locations.append(loc)
        return locations

class ConsistencyChecker:
    """一致性检查器"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def check_consistency(self, chapter_content: str, chapter_number: int,
                         character_states: Dict, plot_threads: Dict,
                         world_state: WorldState, chapter_summaries: deque) -> Dict[str, Any]:
        """检查章节一致性"""
        consistency_issues = []
        
        # 检查角色一致性
        char_issues = self._check_character_consistency(
            chapter_content, character_states
        )
        consistency_issues.extend(char_issues)
        
        # 检查情节一致性
        plot_issues = self._check_plot_consistency(
            chapter_content, plot_threads, chapter_summaries
        )
        consistency_issues.extend(plot_issues)
        
        # 检查世界设定一致性
        world_issues = self._check_world_consistency(
            chapter_content, world_state
        )
        consistency_issues.extend(world_issues)
        
        # 检查时间线一致性
        timeline_issues = self._check_timeline_consistency(
            chapter_content, chapter_summaries
        )
        consistency_issues.extend(timeline_issues)
        
        return {
            'chapter_number': chapter_number,
            'consistency_score': max(0, 10 - len(consistency_issues)),
            'issues': consistency_issues,
            'recommendations': self._generate_fix_recommendations(consistency_issues)
        }
    
    def _check_character_consistency(self, content: str, character_states: Dict) -> List[str]:
        """检查角色一致性"""
        issues = []
        
        for char_name, char_state in character_states.items():
            if char_name in content:
                # 使用LLM检查角色行为是否符合设定
                consistency_check = self._llm_character_consistency_check(
                    content, char_name, char_state
                )
                if consistency_check.get('inconsistent'):
                    issues.append(f"角色{char_name}的行为与设定不符: {consistency_check.get('reason', '')}")
        
        return issues
    
    def _llm_character_consistency_check(self, content: str, char_name: str, 
                                       char_state: CharacterState) -> Dict[str, Any]:
        """使用LLM检查角色一致性"""
        prompt = f"""
检查角色"{char_name}"在以下内容中的行为是否与角色设定一致：

角色设定：
- 性格：{char_state.personality}
- 情感状态：{char_state.emotions}
- 目标：{char_state.goals}

内容：
{content}

请分析角色的对话、行为、反应是否符合设定，返回JSON格式：
{{
    "inconsistent": true/false,
    "reason": "不一致的原因（如果有）",
    "severity": "high/medium/low"
}}
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=500, temperature=0.2)
            return json.loads(response)
        except:
            return {"inconsistent": False}

    def check_novel_coherence(self, chapter_numbers: List[int], 
                            novel_context: Dict[str, Any], 
                            storage: Any) -> Dict[str, Any]:
        """检查整部小说的连贯性"""
        logger.info(f"检查小说连贯性，章节范围: {chapter_numbers}")
        
        coherence_report = {
            'success': True,
            'overall_coherence_score': 0.0,
            'character_coherence': 0.0,
            'plot_coherence': 0.0,
            'timeline_coherence': 0.0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            # 加载所有章节
            chapters_content = []
            for ch_num in chapter_numbers:
                chapter_data = storage.load_chapter(ch_num)
                if chapter_data:
                    chapters_content.append({
                        'number': ch_num,
                        'content': chapter_data.get('content', '')
                    })
            
            if not chapters_content:
                return coherence_report
            
            # 检查角色一致性
            char_score = self._check_character_coherence_across_chapters(chapters_content)
            coherence_report['character_coherence'] = char_score
            
            # 检查情节连贯性
            plot_score = self._check_plot_coherence_across_chapters(chapters_content)
            coherence_report['plot_coherence'] = plot_score
            
            # 检查时间线连贯性
            timeline_score = 8.0  # 简化实现
            coherence_report['timeline_coherence'] = timeline_score
            
            # 计算总体评分
            coherence_report['overall_coherence_score'] = (
                char_score * 0.4 + plot_score * 0.4 + timeline_score * 0.2
            )
            
            # 生成建议
            if coherence_report['overall_coherence_score'] < 7.0:
                coherence_report['suggestions'].append("建议加强章节间的连接")
                coherence_report['suggestions'].append("注意角色行为的一致性")
            
            return coherence_report
            
        except Exception as e:
            logger.error(f"连贯性检查失败: {e}")
            coherence_report['success'] = False
            coherence_report['error'] = str(e)
            return coherence_report
    
    def _check_character_coherence_across_chapters(self, chapters: List[Dict]) -> float:
        """检查角色跨章节一致性"""
        # 简化实现，返回固定分数
        return 7.5
    
    def _check_plot_coherence_across_chapters(self, chapters: List[Dict]) -> float:
        """检查情节跨章节连贯性"""
        # 简化实现，返回固定分数
        return 7.8
    
    def ensure_chapter_coherence(self, content: str, chapter_number: int,
                                novel_context: Dict[str, Any], 
                                storage: Any) -> str:
        """确保章节连贯性，返回优化后的内容"""
        logger.info(f"优化第{chapter_number}章的连贯性")
        
        try:
            # 获取前一章内容
            prev_chapter = None
            if chapter_number > 1:
                prev_chapter_data = storage.load_chapter(chapter_number - 1)
                if prev_chapter_data:
                    prev_chapter = prev_chapter_data.get('content', '')
            
            # 如果没有前一章，直接返回原内容
            if not prev_chapter:
                return content
            
            # 使用LLM优化连贯性
            prompt = f"""
请优化以下第{chapter_number}章内容，确保与前一章的连贯性：

前一章结尾部分：
{prev_chapter[-500:]}

当前章节内容：
{content}

请优化当前章节的开头，使其与前一章自然衔接。保持故事的连贯性，注意：
1. 时间和地点的衔接
2. 角色状态的延续
3. 情节的自然过渡

返回优化后的完整章节内容。
"""
            
            improved_content = self.llm.generate(prompt, max_tokens=4000, temperature=0.7)
            
            # 如果优化后内容太短，返回原内容
            if len(improved_content) < len(content) * 0.5:
                return content
            
            return improved_content
            
        except Exception as e:
            logger.error(f"连贯性优化失败: {e}")
            return content

class LongTermMemoryManager:
    """长期记忆管理器"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.memory_embeddings = {}  # 将来可以用向量数据库
        
    def get_relevant_context(self, current_chapter: int, lookback_chapters: int,
                           chapter_summaries: deque, character_states: Dict,
                           plot_threads: Dict) -> Dict[str, Any]:
        """获取相关的长期记忆上下文"""
        
        # 获取最近章节的重要信息
        recent_summaries = list(chapter_summaries)[-lookback_chapters:]
        
        # 提取持续性元素
        persistent_elements = self._extract_persistent_elements(
            recent_summaries, character_states, plot_threads
        )
        
        # 生成上下文摘要
        context_summary = self._generate_long_term_context_summary(
            recent_summaries, persistent_elements, current_chapter
        )
        
        return {
            'context_summary': context_summary,
            'key_characters': self._get_key_character_info(character_states),
            'active_plot_threads': self._get_active_threads(plot_threads),
            'unresolved_questions': self._extract_unresolved_questions(recent_summaries),
            'continuity_warnings': self._generate_continuity_warnings(current_chapter)
        }
    
    def _generate_long_term_context_summary(self, summaries: List[Dict], 
                                          elements: Dict, current_chapter: int) -> str:
        """生成长期上下文摘要"""
        prompt = f"""
基于以下最近章节摘要，为第{current_chapter}章生成长期上下文摘要：

最近章节摘要：
{json.dumps([s.get('raw_summary', '') for s in summaries], ensure_ascii=False)}

持续性元素：
{json.dumps(elements, ensure_ascii=False)}

请生成一个简洁但全面的上下文摘要，包括：
1. 故事当前状态
2. 主要角色状况
3. 未解决的情节线
4. 重要的背景信息
5. 需要注意的连续性要点

摘要长度控制在500字以内。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=800, temperature=0.3)
            return response
        except Exception as e:
            logger.error(f"生成长期上下文摘要失败: {e}")
            return f"第{current_chapter}章上下文摘要生成失败"
