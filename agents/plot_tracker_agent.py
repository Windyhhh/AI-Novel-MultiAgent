"""情节线索追踪Agent"""
import json
import os
from typing import Dict, List, Optional
from utils import Storage, get_logger

logger = get_logger('plot_tracker')

class PlotTrackerAgent:
    """情节追踪Agent - 管理主线、支线和伏笔"""
    
    def __init__(self):
        self.storage = Storage()
        self.plot_dir = "data/plot_tracking"
        self.plot_file = os.path.join(self.plot_dir, "plot_lines.json")
        self.plot_data = self._load_plot_data()
        logger.info("情节追踪Agent初始化完成")
    
    def _load_plot_data(self) -> Dict:
        """加载情节数据"""
        try:
            if os.path.exists(self.plot_file):
                with open(self.plot_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {
                "main_plot": [],
                "sub_plots": {},
                "foreshadowing": [],
                "conflicts": []
            }
        except Exception as e:
            logger.error(f"加载情节数据失败: {e}")
            return {"main_plot": [], "sub_plots": {}, "foreshadowing": [], "conflicts": []}
    
    def add_plot_point(self, plot_type: str, chapter: int, 
                      description: str, status: str = "ongoing",
                      related_characters: List[str] = None):
        """
        添加情节点
        
        Args:
            plot_type: 情节类型，"main"表示主线，其他为支线名称
            chapter: 章节编号
            description: 情节描述
            status: 状态 (ongoing/resolved/suspended)
            related_characters: 相关角色列表
        """
        plot_point = {
            "chapter": chapter,
            "description": description,
            "status": status,
            "related_characters": related_characters or [],
            "related_foreshadowing": []
        }
        
        if plot_type == "main":
            self.plot_data["main_plot"].append(plot_point)
        else:
            if plot_type not in self.plot_data["sub_plots"]:
                self.plot_data["sub_plots"][plot_type] = []
            self.plot_data["sub_plots"][plot_type].append(plot_point)
        
        self._save_plot_data()
        logger.info(f"添加情节点: {plot_type} - 第{chapter}章")
    
    def add_foreshadowing(self, chapter: int, content: str, 
                         target_chapter: int = None, category: str = "general") -> str:
        """
        添加伏笔
        
        Args:
            chapter: 埋设章节
            content: 伏笔内容
            target_chapter: 目标回收章节
            category: 伏笔类别
        
        Returns:
            伏笔ID
        """
        fh_id = f"fh_{len(self.plot_data['foreshadowing']) + 1:03d}"
        foreshadowing = {
            "id": fh_id,
            "planted_chapter": chapter,
            "content": content,
            "target_chapter": target_chapter,
            "category": category,
            "resolved": False,
            "resolved_chapter": None,
            "resolution_content": ""
        }
        self.plot_data["foreshadowing"].append(foreshadowing)
        self._save_plot_data()
        logger.info(f"添加伏笔: {fh_id} - 第{chapter}章")
        return fh_id
    
    def resolve_foreshadowing(self, fh_id: str, chapter: int, resolution: str = ""):
        """回收伏笔"""
        for fh in self.plot_data["foreshadowing"]:
            if fh["id"] == fh_id:
                fh["resolved"] = True
                fh["resolved_chapter"] = chapter
                fh["resolution_content"] = resolution
                self._save_plot_data()
                logger.info(f"回收伏笔: {fh_id} - 第{chapter}章")
                break
    
    def get_unresolved_foreshadowing(self, up_to_chapter: int = None) -> List[Dict]:
        """获取未回收的伏笔"""
        unresolved = [fh for fh in self.plot_data["foreshadowing"] if not fh["resolved"]]
        if up_to_chapter:
            unresolved = [fh for fh in unresolved if fh["planted_chapter"] <= up_to_chapter]
        return unresolved
    
    def add_conflict(self, chapter: int, conflict_type: str, 
                    description: str, parties: List[str]):
        """
        添加冲突
        
        Args:
            chapter: 章节编号
            conflict_type: 冲突类型 (character/internal/external/social)
            description: 冲突描述
            parties: 冲突各方
        """
        conflict = {
            "chapter": chapter,
            "type": conflict_type,
            "description": description,
            "parties": parties,
            "resolved": False
        }
        self.plot_data["conflicts"].append(conflict)
        self._save_plot_data()
        logger.info(f"添加冲突: {conflict_type} - 第{chapter}章")
    
    def get_plot_summary(self, up_to_chapter: int = None) -> str:
        """获取情节摘要"""
        summary = "【主线情节】\n"
        for point in self.plot_data["main_plot"]:
            if up_to_chapter is None or point["chapter"] <= up_to_chapter:
                summary += f"第{point['chapter']}章: {point['description']} [{point['status']}]\n"
        
        if self.plot_data["sub_plots"]:
            summary += "\n【支线情节】\n"
            for plot_name, points in self.plot_data["sub_plots"].items():
                summary += f"\n{plot_name}:\n"
                for point in points:
                    if up_to_chapter is None or point["chapter"] <= up_to_chapter:
                        summary += f"  第{point['chapter']}章: {point['description']} [{point['status']}]\n"
        
        return summary

    def get_foreshadowing_reminder(self, current_chapter: int) -> str:
        """获取伏笔提醒"""
        unresolved = self.get_unresolved_foreshadowing(current_chapter)
        if not unresolved:
            return ""

        reminder = "【待回收伏笔提醒】\n"
        for fh in unresolved:
            chapters_ago = current_chapter - fh["planted_chapter"]
            reminder += f"- {fh['content']} (第{fh['planted_chapter']}章埋设，已过{chapters_ago}章)\n"
            if fh['target_chapter'] and current_chapter >= fh['target_chapter']:
                reminder += f"  ⚠️ 建议在本章回收！\n"
        return reminder

    def _save_plot_data(self):
        """保存情节数据"""
        try:
            os.makedirs(self.plot_dir, exist_ok=True)
            with open(self.plot_file, 'w', encoding='utf-8') as f:
                json.dump(self.plot_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存情节数据失败: {e}")

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "main_plot_points": len(self.plot_data["main_plot"]),
            "sub_plots_count": len(self.plot_data["sub_plots"]),
            "total_foreshadowing": len(self.plot_data["foreshadowing"]),
            "unresolved_foreshadowing": len([fh for fh in self.plot_data["foreshadowing"] if not fh["resolved"]]),
            "total_conflicts": len(self.plot_data["conflicts"])
        }

