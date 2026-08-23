"""角色记忆与一致性管理Agent"""
import json
import os
from typing import Dict, List, Optional
from utils import Storage, LLMClient, get_logger

logger = get_logger('character_memory')

class CharacterMemoryAgent:
    """角色记忆管理Agent - 确保角色行为的一致性"""
    
    def __init__(self):
        self.storage = Storage()
        self.llm = LLMClient()
        self.memory_dir = "data/character_memory"
        self.memory_file = os.path.join(self.memory_dir, "characters.json")
        self.characters = self._load_characters()
        logger.info("角色记忆Agent初始化完成")
    
    def _load_characters(self) -> Dict:
        """加载角色数据"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"加载角色数据失败: {e}")
            return {}
    
    def add_character(self, character_data: Dict) -> str:
        """
        添加新角色
        
        Args:
            character_data: 角色信息字典，包含name, personality_traits等
        
        Returns:
            角色ID
        """
        char_id = f"char_{len(self.characters) + 1:03d}"
        self.characters[char_id] = {
            "id": char_id,
            "name": character_data.get("name"),
            "personality_traits": character_data.get("personality_traits", []),
            "appearance": character_data.get("appearance", ""),
            "background": character_data.get("background", ""),
            "speech_patterns": character_data.get("speech_patterns", []),
            "relationships": character_data.get("relationships", {}),
            "behavior_history": [],
            "development_arc": character_data.get("development_arc", ""),
            "current_state": character_data.get("current_state", {
                "location": "",
                "emotion": "",
                "goal": ""
            })
        }
        self._save_characters()
        logger.info(f"添加角色: {character_data.get('name')} (ID: {char_id})")
        return char_id
    
    def update_character(self, char_id: str, updates: Dict):
        """更新角色信息"""
        if char_id in self.characters:
            self.characters[char_id].update(updates)
            self._save_characters()
            logger.info(f"更新角色: {char_id}")
    
    def record_behavior(self, char_id: str, chapter: int, action: str, 
                       emotion: str, context: str):
        """
        记录角色行为
        
        Args:
            char_id: 角色ID
            chapter: 章节编号
            action: 行为描述
            emotion: 情绪状态
            context: 上下文情境
        """
        if char_id in self.characters:
            behavior = {
                "chapter": chapter,
                "action": action,
                "emotion": emotion,
                "context": context
            }
            self.characters[char_id]["behavior_history"].append(behavior)
            
            # 只保留最近20条记录
            if len(self.characters[char_id]["behavior_history"]) > 20:
                self.characters[char_id]["behavior_history"] = \
                    self.characters[char_id]["behavior_history"][-20:]
            
            self._save_characters()
            logger.debug(f"记录角色行为: {char_id} - {action}")
    
    def check_consistency(self, char_id: str, proposed_action: str, 
                         context: str) -> Dict:
        """
        检查角色行为一致性
        
        Args:
            char_id: 角色ID
            proposed_action: 拟定的行为
            context: 当前情境
        
        Returns:
            一致性检查结果
        """
        if char_id not in self.characters:
            return {"consistent": True, "warning": None}
        
        character = self.characters[char_id]
        
        # 构建检查提示词
        prompt = f"""
你是一个专业的小说编辑，负责检查角色行为的一致性。

【角色档案】
姓名：{character['name']}
性格特征：{', '.join(character['personality_traits'])}
说话方式：{', '.join(character['speech_patterns'])}

【最近行为历史】
{json.dumps(character['behavior_history'][-5:], ensure_ascii=False, indent=2)}

【当前情境】
{context}

【拟定行为】
{proposed_action}

请评估该行为是否符合角色设定。如果不符合，请说明原因并给出建议。

返回JSON格式：
{{
    "consistent": true/false,
    "confidence": 0.0-1.0,
    "reason": "评估原因",
    "suggestion": "改进建议（如果不一致）"
}}
"""
        
        try:
            response = self.llm.chat([{"role": "user", "content": prompt}])
            result = json.loads(response)
            logger.info(f"一致性检查: {char_id} - {result.get('consistent')}")
            return result
        except Exception as e:
            logger.error(f"一致性检查失败: {e}")
            return {"consistent": True, "warning": f"检查失败: {str(e)}"}

    def get_character_context(self, char_id: str, max_history: int = 3) -> str:
        """获取角色上下文信息（用于注入到生成提示词）"""
        if char_id not in self.characters:
            return ""

        character = self.characters[char_id]
        context = f"""
【角色：{character['name']}】
- 性格：{', '.join(character['personality_traits'])}
- 外貌：{character['appearance']}
- 说话方式：{', '.join(character['speech_patterns'])}
"""
        if character['behavior_history']:
            context += "\n- 最近行为：\n"
            for behavior in character['behavior_history'][-max_history:]:
                context += f"  第{behavior['chapter']}章: {behavior['action']}\n"
        return context

    def get_all_characters(self) -> List[Dict]:
        """获取所有角色列表"""
        return list(self.characters.values())

    def get_character_by_name(self, name: str) -> Optional[Dict]:
        """根据名字获取角色"""
        for char in self.characters.values():
            if char['name'] == name:
                return char
        return None

    def extract_characters_from_outline(self, outline: Dict) -> List[str]:
        """从大纲中提取角色并自动创建记忆"""
        char_ids = []
        main_characters = outline.get('main_characters', [])
        for char_data in main_characters:
            existing = self.get_character_by_name(char_data.get('name'))
            if existing:
                char_ids.append(existing['id'])
                continue
            char_id = self.add_character({
                "name": char_data.get('name', '未命名'),
                "personality_traits": char_data.get('personality', '').split('、'),
                "appearance": char_data.get('appearance', ''),
                "background": char_data.get('background', ''),
                "speech_patterns": [],
                "relationships": {},
                "development_arc": char_data.get('character_arc', '')
            })
            char_ids.append(char_id)
        logger.info(f"从大纲提取了 {len(char_ids)} 个角色")
        return char_ids

    def _save_characters(self):
        """保存角色数据"""
        try:
            os.makedirs(self.memory_dir, exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.characters, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存角色数据失败: {e}")

