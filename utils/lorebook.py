"""世界观知识库系统（Lorebook）"""
import json
import os
from typing import List, Dict, Optional
from utils import get_logger

logger = get_logger('lorebook')

class Lorebook:
    """世界观知识库 - 管理设定、专有名词、规则体系"""
    
    def __init__(self, lorebook_dir: str = "data/lorebook"):
        self.lorebook_dir = lorebook_dir
        self.entries_file = os.path.join(lorebook_dir, "entries.json")
        self.entries = self._load_entries()
        logger.info(f"Lorebook初始化完成，共{len(self.entries)}个词条")
    
    def _load_entries(self) -> List[Dict]:
        """加载词条"""
        try:
            if os.path.exists(self.entries_file):
                with open(self.entries_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"加载词条失败: {e}")
            return []
    
    def add_entry(self, title: str, category: str, content: str, 
                  triggers: List[str], priority: int = 5, 
                  always_active: bool = False) -> str:
        """
        添加词条
        
        Args:
            title: 词条标题
            category: 类别 (地点/人物/物品/技能/组织/规则等)
            content: 词条内容
            triggers: 触发词列表
            priority: 优先级 (1-10，越高越优先)
            always_active: 是否始终激活
        
        Returns:
            词条ID
        """
        entry_id = f"entry_{len(self.entries) + 1:03d}"
        entry = {
            "id": entry_id,
            "title": title,
            "category": category,
            "content": content,
            "triggers": triggers,
            "priority": priority,
            "always_active": always_active
        }
        self.entries.append(entry)
        self._save_entries()
        logger.info(f"添加词条: {title} (ID: {entry_id})")
        return entry_id
    
    def update_entry(self, entry_id: str, updates: Dict):
        """更新词条"""
        for entry in self.entries:
            if entry["id"] == entry_id:
                entry.update(updates)
                self._save_entries()
                logger.info(f"更新词条: {entry_id}")
                return True
        return False
    
    def delete_entry(self, entry_id: str):
        """删除词条"""
        self.entries = [e for e in self.entries if e["id"] != entry_id]
        self._save_entries()
        logger.info(f"删除词条: {entry_id}")
    
    def get_relevant_entries(self, text: str, max_entries: int = 5) -> List[Dict]:
        """
        获取相关词条
        
        Args:
            text: 当前文本内容
            max_entries: 最多返回的词条数
        
        Returns:
            相关词条列表
        """
        relevant = []
        
        # 首先添加always_active的词条
        for entry in self.entries:
            if entry["always_active"]:
                relevant.append(entry)
        
        # 然后根据触发词匹配
        for entry in self.entries:
            if entry["always_active"]:
                continue
            for trigger in entry["triggers"]:
                if trigger in text:
                    relevant.append(entry)
                    break
        
        # 按优先级排序
        relevant.sort(key=lambda x: x["priority"], reverse=True)
        
        return relevant[:max_entries]
    
    def get_entries_by_category(self, category: str) -> List[Dict]:
        """根据类别获取词条"""
        return [e for e in self.entries if e["category"] == category]
    
    def search_entries(self, keyword: str) -> List[Dict]:
        """搜索词条"""
        results = []
        keyword_lower = keyword.lower()
        for entry in self.entries:
            if (keyword_lower in entry["title"].lower() or 
                keyword_lower in entry["content"].lower() or
                any(keyword_lower in t.lower() for t in entry["triggers"])):
                results.append(entry)
        return results
    
    def format_context(self, entries: List[Dict]) -> str:
        """
        格式化为上下文
        
        Args:
            entries: 词条列表
        
        Returns:
            格式化的上下文字符串
        """
        if not entries:
            return ""
        
        context = "【世界观设定】\n"
        for entry in entries:
            context += f"\n【{entry['title']}】（{entry['category']}）\n"
            context += f"{entry['content']}\n"
        
        return context
    
    def extract_from_outline(self, outline: Dict) -> List[str]:
        """从大纲中提取并创建词条"""
        entry_ids = []
        
        # 提取世界观设定
        world_setting = outline.get('world_setting', '')
        if world_setting:
            entry_id = self.add_entry(
                title="世界观总览",
                category="世界设定",
                content=world_setting,
                triggers=["世界", "设定"],
                priority=10,
                always_active=True
            )
            entry_ids.append(entry_id)
        
        logger.info(f"从大纲提取了 {len(entry_ids)} 个词条")
        return entry_ids
    
    def _save_entries(self):
        """保存词条"""
        try:
            os.makedirs(self.lorebook_dir, exist_ok=True)
            with open(self.entries_file, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存词条失败: {e}")

