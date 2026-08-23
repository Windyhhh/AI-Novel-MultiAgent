"""
智能体工厂
动态创建和管理不同类型的小说智能体，方便扩展新的智能体类型
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Type, Callable
from utils import LLMClient, get_logger, Storage

logger = get_logger('agent_factory')

class AgentFactory:
    """智能体工厂"""
    
    def __init__(self):
        self.storage = Storage()
        self.llm = LLMClient()
        self.registered_agents = {}
        self.agent_instances = {}
        self.genre_mappings = {}
        
        # 注册内置智能体类型
        self._register_builtin_agents()
    
    def _register_builtin_agents(self):
        """注册内置智能体类型"""
        from .mystery_agent import MysteryAgent
        from .tomato_novel_agent import TomatoNovelAgent
        from .outline_agent import OutlineAgent
        from .chapter_planning_agent import ChapterPlanningAgent
        from .content_generation_agent import ContentGenerationAgent
        from .character_memory_agent import CharacterMemoryAgent
        from .plot_tracker_agent import PlotTrackerAgent
        
        # 注册基础智能体
        self.register_agent_type('mystery', MysteryAgent, ['悬疑', '推理', 'mystery'])
        self.register_agent_type('tomato_novel', TomatoNovelAgent, ['番茄小说', '网文'])
        self.register_agent_type('outline', OutlineAgent, ['大纲', 'outline'])
        self.register_agent_type('chapter_planning', ChapterPlanningAgent, ['章节规划'])
        self.register_agent_type('content_generation', ContentGenerationAgent, ['内容生成'])
        self.register_agent_type('character_memory', CharacterMemoryAgent, ['角色记忆'])
        self.register_agent_type('plot_tracker', PlotTrackerAgent, ['情节追踪'])
        
        # 注册新的智能体类型（占位符，实际需要创建对应的类）
        self.register_agent_type('romance', self._create_romance_agent, ['言情', '恋爱', 'romance'])
        self.register_agent_type('fantasy', self._create_fantasy_agent, ['奇幻', '玄幻', 'fantasy'])
        self.register_agent_type('scifi', self._create_scifi_agent, ['科幻', '未来', 'scifi'])
        self.register_agent_type('historical', self._create_historical_agent, ['历史', '古代'])
        self.register_agent_type('urban', self._create_urban_agent, ['都市', '现代'])
    
    def register_agent_type(self, agent_name: str, agent_class: Type, genres: List[str]):
        """注册智能体类型"""
        self.registered_agents[agent_name] = agent_class
        
        # 建立类型映射
        for genre in genres:
            self.genre_mappings[genre.lower()] = agent_name
        
        logger.info(f"注册智能体类型: {agent_name}, 适用类型: {genres}")
    
    def get_agent(self, agent_name: str, **kwargs):
        """获取智能体实例"""
        if agent_name in self.agent_instances:
            return self.agent_instances[agent_name]
        
        if agent_name not in self.registered_agents:
            logger.error(f"未注册的智能体类型: {agent_name}")
            return None
        
        try:
            agent_class = self.registered_agents[agent_name]
            
            # 如果是函数，调用函数创建智能体
            if callable(agent_class) and not isinstance(agent_class, type):
                agent_instance = agent_class(**kwargs)
            else:
                # 如果是类，实例化
                agent_instance = agent_class(**kwargs)
            
            self.agent_instances[agent_name] = agent_instance
            logger.info(f"创建智能体实例: {agent_name}")
            
            return agent_instance
        
        except Exception as e:
            logger.error(f"创建智能体失败 {agent_name}: {e}")
            return None
    
    def get_agent_by_genre(self, genre: str, **kwargs):
        """根据小说类型获取合适的智能体"""
        agent_name = self.genre_mappings.get(genre.lower())
        
        if not agent_name:
            # 使用默认的内容生成智能体
            agent_name = 'content_generation'
        
        return self.get_agent(agent_name, **kwargs)
    
    def create_collaborative_agents(self, genre: str, platform: str = 'tomato_novel') -> Dict[str, Any]:
        """为特定类型创建协作智能体组合"""
        agents = {}
        
        # 基础智能体
        agents['outline'] = self.get_agent('outline')
        agents['chapter_planning'] = self.get_agent('chapter_planning')
        agents['character_memory'] = self.get_agent('character_memory')
        agents['plot_tracker'] = self.get_agent('plot_tracker')
        
        # 根据类型添加专用智能体
        if genre.lower() in ['悬疑', '推理', 'mystery']:
            agents['mystery'] = self.get_agent('mystery')
        elif genre.lower() in ['言情', '恋爱', 'romance']:
            agents['romance'] = self.get_agent('romance')
        elif genre.lower() in ['奇幻', '玄幻', 'fantasy']:
            agents['fantasy'] = self.get_agent('fantasy')
        elif genre.lower() in ['科幻', '未来', 'scifi']:
            agents['scifi'] = self.get_agent('scifi')
        elif genre.lower() in ['历史', '古代']:
            agents['historical'] = self.get_agent('historical')
        elif genre.lower() in ['都市', '现代']:
            agents['urban'] = self.get_agent('urban')
        
        # 通用内容生成智能体
        agents['content_generation'] = self.get_agent('content_generation')
        
        # 根据平台添加优化智能体
        if platform == 'tomato_novel':
            agents['tomato_novel'] = self.get_agent('tomato_novel')
        
        logger.info(f"为{genre}类型创建协作智能体组合: {list(agents.keys())}")
        return agents
    
    def list_available_agents(self) -> Dict[str, Any]:
        """列出所有可用的智能体"""
        return {
            'registered_agents': list(self.registered_agents.keys()),
            'genre_mappings': self.genre_mappings,
            'active_instances': list(self.agent_instances.keys())
        }
    
    def _create_romance_agent(self, **kwargs):
        """创建言情小说智能体"""
        return RomanceAgent()
    
    def _create_fantasy_agent(self, **kwargs):
        """创建玄幻小说智能体"""
        return FantasyAgent()
    
    def _create_scifi_agent(self, **kwargs):
        """创建科幻小说智能体"""
        return SciFiAgent()
    
    def _create_historical_agent(self, **kwargs):
        """创建历史小说智能体"""
        return HistoricalAgent()
    
    def _create_urban_agent(self, **kwargs):
        """创建都市小说智能体"""
        return UrbanAgent()

class BaseGenreAgent:
    """基础类型智能体"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.storage = Storage()
        self.genre_name = "通用"
        self.genre_characteristics = {}
    
    def create_outline(self, custom_settings: Dict[str, Any]) -> Dict[str, Any]:
        """创建该类型的大纲"""
        prompt = f"""
作为{self.genre_name}小说专家，请创建一个专业的小说大纲。

用户设定：
{json.dumps(custom_settings, ensure_ascii=False, indent=2)}

{self.genre_name}小说特点：
{json.dumps(self.genre_characteristics, ensure_ascii=False, indent=2)}

请创建包含以下内容的大纲：
1. 基本设定（书名、主题、背景）
2. 角色设定（主要角色及其特点）
3. 情节结构（开头、发展、高潮、结局）
4. 特色元素（该类型的独特要素）
5. 章节规划（预计章节数和主要情节点）

确保大纲符合{self.genre_name}小说的规范和读者期待。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=3500, temperature=0.8)
            
            outline = {
                'id': f"{self.genre_name.lower()}_{int(datetime.now().timestamp())}",
                'genre': self.genre_name,
                'created_at': datetime.now().isoformat(),
                'raw_outline': response,
                'custom_settings': custom_settings,
                'characteristics': self.genre_characteristics
            }
            
            return outline
            
        except Exception as e:
            logger.error(f"创建{self.genre_name}大纲失败: {e}")
            return None
    
    def generate_chapter(self, chapter_plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """生成该类型的章节"""
        chapter_number = chapter_plan.get('chapter_number', 1)
        
        prompt = f"""
作为{self.genre_name}小说专家，请生成第{chapter_number}章内容。

章节规划：
{json.dumps(chapter_plan, ensure_ascii=False, indent=2)}

小说上下文：
{json.dumps(context, ensure_ascii=False, indent=2)}

{self.genre_name}写作要求：
{json.dumps(self.genre_characteristics, ensure_ascii=False, indent=2)}

章节要求：
- 字数：2500-3000字
- 体现{self.genre_name}小说特色
- 情节推进自然
- 人物塑造深入
- 语言风格统一

请生成完整的章节内容。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=4000, temperature=0.8)
            
            return {
                'chapter_number': chapter_number,
                'content': response,
                'word_count': len(response),
                'genre': self.genre_name,
                'generated_at': datetime.now().isoformat(),
                'plan': chapter_plan
            }
            
        except Exception as e:
            logger.error(f"生成{self.genre_name}第{chapter_number}章失败: {e}")
            return None

class RomanceAgent(BaseGenreAgent):
    """言情小说智能体"""
    
    def __init__(self):
        super().__init__()
        self.genre_name = "言情"
        self.genre_characteristics = {
            "核心要素": ["情感发展", "角色关系", "浪漫情节", "情感冲突"],
            "情节模式": ["初遇", "误会", "磨合", "分离", "重逢", "圆满"],
            "写作重点": ["情感描写", "心理活动", "对话互动", "细节刻画"],
            "常见设定": ["霸道总裁", "校园恋情", "重生穿越", "豪门世家"],
            "读者期待": ["甜宠互动", "情感共鸣", "幸福结局", "代入感强"]
        }
    
    def analyze_relationship_development(self, content: str, characters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析情感关系发展"""
        # 实现情感关系分析逻辑
        return {"relationship_stage": "发展期", "emotional_intensity": 7.5}

class FantasyAgent(BaseGenreAgent):
    """玄幻小说智能体"""
    
    def __init__(self):
        super().__init__()
        self.genre_name = "玄幻"
        self.genre_characteristics = {
            "核心要素": ["修炼体系", "境界等级", "法宝神通", "异世界观"],
            "情节模式": ["废材逆袭", "奇遇获宝", "仇人追杀", "宗门比试", "历练成长"],
            "写作重点": ["世界观构建", "力量体系", "战斗描写", "升级爽感"],
            "常见设定": ["修仙世界", "异界大陆", "灵气修炼", "古老传承"],
            "读者期待": ["爽点密集", "实力提升", "打脸情节", "宏大场面"]
        }
    
    def create_cultivation_system(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """创建修炼体系"""
        # 实现修炼体系创建逻辑
        return {"levels": ["练气", "筑基", "金丹", "元婴"], "system": "仙道"}

class SciFiAgent(BaseGenreAgent):
    """科幻小说智能体"""
    
    def __init__(self):
        super().__init__()
        self.genre_name = "科幻"
        self.genre_characteristics = {
            "核心要素": ["科技设定", "未来世界", "科学理论", "技术发展"],
            "情节模式": ["科技革命", "宇宙探索", "人工智能", "时空穿越", "生物进化"],
            "写作重点": ["科技描写", "逻辑严谨", "想象力", "社会思考"],
            "常见设定": ["星际文明", "机甲战士", "虚拟现实", "基因改造"],
            "读者期待": ["科技感", "逻辑性", "预见性", "思辨性"]
        }

class HistoricalAgent(BaseGenreAgent):
    """历史小说智能体"""
    
    def __init__(self):
        super().__init__()
        self.genre_name = "历史"
        self.genre_characteristics = {
            "核心要素": ["历史背景", "人物传记", "政治斗争", "文化展现"],
            "情节模式": ["朝堂争斗", "军事征战", "商业传奇", "文人墨客"],
            "写作重点": ["历史考证", "人物刻画", "时代特色", "文化底蕴"],
            "常见设定": ["朝代更替", "英雄人物", "历史事件", "民俗风情"],
            "读者期待": ["真实感", "代入感", "历史知识", "人物魅力"]
        }

class UrbanAgent(BaseGenreAgent):
    """都市小说智能体"""
    
    def __init__(self):
        super().__init__()
        self.genre_name = "都市"
        self.genre_characteristics = {
            "核心要素": ["现代生活", "职场商战", "都市情感", "现实题材"],
            "情节模式": ["逆袭成功", "商业竞争", "情感纠葛", "家庭伦理"],
            "写作重点": ["现实感", "职场描写", "情感戏份", "社会现象"],
            "常见设定": ["商业精英", "都市白领", "创业故事", "豪门恩怨"],
            "读者期待": ["代入感", "成功感", "现实意义", "情感共鸣"]
        }

class GenreAgentRegistry:
    """类型智能体注册表"""
    
    def __init__(self):
        self.agents = {}
        self.factory = AgentFactory()
    
    def register_custom_agent(self, genre: str, agent_class: Type, keywords: List[str]):
        """注册自定义智能体"""
        self.factory.register_agent_type(genre, agent_class, keywords)
        logger.info(f"注册自定义智能体: {genre}")
    
    def get_suitable_agents(self, requirements: Dict[str, Any]) -> List[str]:
        """根据需求获取合适的智能体"""
        genre = requirements.get('genre', '').lower()
        platform = requirements.get('platform', '').lower()
        style = requirements.get('style', '').lower()
        
        suitable_agents = []
        
        # 根据类型选择
        if genre in self.factory.genre_mappings:
            suitable_agents.append(self.factory.genre_mappings[genre])
        
        # 根据平台选择
        if platform == 'tomato_novel' or '番茄' in platform:
            suitable_agents.append('tomato_novel')
        
        # 总是包含基础智能体
        suitable_agents.extend(['outline', 'chapter_planning', 'character_memory', 'plot_tracker'])
        
        return list(set(suitable_agents))  # 去重
