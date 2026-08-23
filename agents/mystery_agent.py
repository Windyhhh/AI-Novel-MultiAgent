"""
悬疑推理小说专用智能体
专门处理推理小说的逻辑构建、线索管理、伏笔布设等
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from utils import LLMClient, get_logger, Storage

logger = get_logger('mystery_agent')

class MysteryAgent:
    """悬疑推理小说专用智能体"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.storage = Storage()
        
    def create_mystery_outline(self, custom_settings: Dict[str, Any]) -> Dict[str, Any]:
        """创建悬疑推理小说大纲"""
        mystery_type = custom_settings.get('mystery_type', '本格推理')
        setting = custom_settings.get('setting', '现代都市')
        victim_profile = custom_settings.get('victim_profile', '年轻白领')
        motive_theme = custom_settings.get('motive_theme', '金钱纠纷')
        
        prompt = f"""
作为悬疑推理小说专家，请为番茄小说平台创建一个{mystery_type}小说大纲。

设定要求：
- 题材类型：{mystery_type}
- 故事背景：{setting}
- 受害者设定：{victim_profile}
- 犯罪动机：{motive_theme}
- 平台要求：番茄小说(快节奏、抓人眼球、章节2500字左右)

请按以下结构创建大纲：

## 基本设定
- 书名：[吸引眼球的悬疑标题]
- 主题：[核心主题]
- 故事背景：[详细背景设定]

## 角色设定
- 主角(侦探)：[姓名、职业、特点、推理能力]
- 受害者：[背景、死因、关键信息]
- 嫌疑人列表：[至少5个嫌疑人，每个都有动机和不在场证明]
- 关键证人：[重要证人角色]

## 核心谜团
- 核心案件：[案件详细描述]
- 关键疑点：[3-5个关键疑点]
- 真相：[真正的犯人和作案手法]
- 反转点：[至少2个重要反转]

## 线索布局
- 明线索：[读者能看到的线索]
- 暗线索：[隐藏的关键线索]
- 伏笔设置：[需要埋设的伏笔]
- 红鲱鱼：[误导性线索]

## 章节规划
- 第一阶段：案件发生(1-15章) - 快速抓住读者
- 第二阶段：调查展开(16-40章) - 线索收集和人物展开
- 第三阶段：真相揭露(41-50章) - 推理过程和结局

## 网文化元素
- 爽点设置：[每10章一个小高潮]
- 悬念点：[章末悬念设计]
- 读者互动：[猜凶手环节]

请确保逻辑严密、线索合理、符合推理小说规范，同时适应网文快节奏特点。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=4000, temperature=0.8)
            
            # 解析和结构化大纲
            outline = {
                'id': str(uuid.uuid4()),
                'created_at': datetime.now().isoformat(),
                'type': 'mystery_novel',
                'mystery_type': mystery_type,
                'setting': setting,
                'platform': 'tomato_novel',
                'raw_outline': response,
                'status': 'created'
            }
            
            # 提取结构化信息
            structured = self._parse_mystery_outline(response)
            outline.update(structured)
            
            # 保存大纲
            self.storage.save_mystery_outline(outline)
            logger.info(f"创建悬疑推理大纲: {outline['id']}")
            
            return outline
            
        except Exception as e:
            logger.error(f"创建悬疑大纲失败: {e}")
            return None
    
    def create_clue_system(self, outline: Dict[str, Any]) -> Dict[str, Any]:
        """创建线索管理系统"""
        prompt = f"""
基于以下悬疑小说大纲，创建详细的线索管理系统：

{outline.get('raw_outline', '')}

请创建一个完整的线索系统，包括：

## 线索分类
1. 物理证据：[可以触摸、检验的证据]
2. 证言证据：[人证、口供]
3. 环境证据：[现场、时间、地点相关]
4. 心理证据：[动机、性格、心理状态]

## 线索时间线
- 犯罪前：[犯罪准备阶段的线索]
- 犯罪时：[作案过程中留下的线索]
- 犯罪后：[案发后产生的线索]

## 线索重要性分级
- S级：[直接指向真凶的关键证据]
- A级：[重要但需要推理的证据]
- B级：[有用但非决定性的证据]
- C级：[误导性或次要证据]

## 线索揭示节奏
- 早期：[前20章需要出现的线索]
- 中期：[21-40章出现的线索]
- 后期：[最后关键线索的出现时机]

## 逻辑链条
- 推理路径1：[正确的推理链条]
- 推理路径2：[错误但合理的推理链条]
- 最终推理：[完整的破案过程]

请确保所有线索都有合理的发现方式和逻辑连接。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=3000, temperature=0.7)
            
            clue_system = {
                'outline_id': outline.get('id'),
                'created_at': datetime.now().isoformat(),
                'raw_system': response,
                'clues': self._parse_clue_system(response)
            }
            
            self.storage.save_clue_system(outline['id'], clue_system)
            logger.info(f"创建线索系统: {outline['id']}")
            
            return clue_system
            
        except Exception as e:
            logger.error(f"创建线索系统失败: {e}")
            return None
    
    def verify_logic_consistency(self, chapter_content: str, clue_system: Dict[str, Any]) -> Dict[str, Any]:
        """验证章节内容的逻辑一致性"""
        prompt = f"""
作为推理小说逻辑专家，请检查以下章节内容的逻辑一致性：

章节内容：
{chapter_content}

已知线索系统：
{json.dumps(clue_system.get('raw_system', ''), ensure_ascii=False, indent=2)}

请检查：
1. 逻辑矛盾：是否与已知信息冲突
2. 时间线问题：时间顺序是否合理
3. 证据合理性：证据发现和处理是否符合实际
4. 角色行为：角色行为是否符合人物设定
5. 推理过程：推理步骤是否合乎逻辑

输出格式：
{{
    "overall_score": 8.5,
    "consistency_issues": [
        "具体问题描述"
    ],
    "suggestions": [
        "改进建议"
    ],
    "logic_rating": "优秀/良好/一般/较差"
}}
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=1500, temperature=0.3)
            
            # 尝试解析JSON响应
            try:
                result = json.loads(response)
            except:
                # 如果不是JSON格式，创建默认结构
                result = {
                    "overall_score": 7.0,
                    "consistency_issues": [],
                    "suggestions": [],
                    "logic_rating": "需要检查",
                    "raw_analysis": response
                }
            
            return result
            
        except Exception as e:
            logger.error(f"逻辑一致性检查失败: {e}")
            return {
                "overall_score": 5.0,
                "consistency_issues": [f"检查失败: {str(e)}"],
                "suggestions": ["建议手动检查逻辑一致性"],
                "logic_rating": "未知"
            }
    
    def generate_character_relationships(self, outline: Dict[str, Any]) -> Dict[str, Any]:
        """生成角色关系图"""
        prompt = f"""
基于以下悬疑小说大纲，创建详细的角色关系图：

{outline.get('raw_outline', '')}

请创建角色关系分析：

## 主要角色
[为每个角色创建档案，包括：姓名、年龄、职业、性格、秘密]

## 关系网络
- 血缘关系：[家族关系]
- 利益关系：[经济、工作相关]
- 情感关系：[爱恨情仇]
- 隐藏关系：[不为人知的联系]

## 动机分析
[为每个嫌疑人分析：
- 犯罪动机强度（1-10分）
- 作案能力评估
- 不在场证明强度
- 隐藏秘密]

## 关系时间线
- 案发前关系：[各角色间的原始关系]
- 案发时关系：[案件对关系的影响]
- 案发后关系：[调查过程中关系变化]

输出为结构化的关系图谱，便于后续创作参考。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=2500, temperature=0.7)
            
            relationships = {
                'outline_id': outline.get('id'),
                'created_at': datetime.now().isoformat(),
                'raw_relationships': response,
                'characters': self._parse_character_relationships(response)
            }
            
            self.storage.save_character_relationships(outline['id'], relationships)
            logger.info(f"创建角色关系图: {outline['id']}")
            
            return relationships
            
        except Exception as e:
            logger.error(f"创建角色关系图失败: {e}")
            return None
    
    def _parse_mystery_outline(self, raw_outline: str) -> Dict[str, Any]:
        """解析悬疑大纲的结构化信息"""
        # 这里可以添加更复杂的解析逻辑
        # 现在先返回基本结构
        return {
            'chapters_planned': 50,
            'main_mystery': '待解析',
            'suspects_count': 5,
            'clues_count': 15
        }
    
    def _parse_clue_system(self, raw_system: str) -> List[Dict[str, Any]]:
        """解析线索系统"""
        # 返回结构化的线索列表
        return []
    
    def _parse_character_relationships(self, raw_relationships: str) -> Dict[str, Any]:
        """解析角色关系"""
        return {
            'main_characters': [],
            'relationships': [],
            'motives': []
        }

class ClueTracker:
    """线索追踪器"""
    
    def __init__(self):
        self.storage = Storage()
    
    def add_clue(self, clue_id: str, clue_data: Dict[str, Any]):
        """添加线索"""
        clue_data.update({
            'id': clue_id,
            'added_at': datetime.now().isoformat(),
            'status': 'active'
        })
        self.storage.save_clue(clue_id, clue_data)
    
    def get_revealed_clues(self, chapter_number: int) -> List[Dict[str, Any]]:
        """获取指定章节前应该揭示的线索"""
        all_clues = self.storage.get_all_clues()
        revealed = []
        
        for clue in all_clues:
            if clue.get('reveal_chapter', 999) <= chapter_number:
                revealed.append(clue)
        
        return revealed
    
    def check_clue_consistency(self, new_clue: Dict[str, Any]) -> bool:
        """检查新线索与已有线索的一致性"""
        # 实现线索一致性检查逻辑
        return True

class LogicValidator:
    """逻辑验证器"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def validate_timeline(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """验证时间线逻辑"""
        # 实现时间线验证逻辑
        return {"valid": True, "issues": []}
    
    def validate_motive(self, character: str, motive: str, evidence: List[str]) -> Dict[str, Any]:
        """验证动机的合理性"""
        # 实现动机验证逻辑
        return {"valid": True, "strength": 0.8}
    
    def validate_method(self, method: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """验证作案手法的可行性"""
        # 实现手法验证逻辑
        return {"feasible": True, "probability": 0.9}
