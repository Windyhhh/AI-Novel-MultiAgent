"""数据存储工具"""
import os
import json
from datetime import datetime
from .config_loader import config

class Storage:
    """数据存储管理类"""
    
    def __init__(self):
        self.novel_dir = config.get('storage.novel_dir', 'data/novels')
        self.outline_file = config.get('storage.outline_file', 'data/outline.json')
        self.chapters_dir = config.get('storage.chapters_dir', 'data/chapters')
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保必要的目录存在"""
        os.makedirs(self.novel_dir, exist_ok=True)
        os.makedirs(self.chapters_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.outline_file), exist_ok=True)
    
    def save_outline(self, outline_data):
        """保存小说大纲"""
        with open(self.outline_file, 'w', encoding='utf-8') as f:
            json.dump(outline_data, f, ensure_ascii=False, indent=2)
    
    def load_outline(self):
        """加载小说大纲"""
        if os.path.exists(self.outline_file):
            with open(self.outline_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_chapter(self, chapter_number, chapter_data):
        """
        保存章节内容
        
        Args:
            chapter_number: 章节编号
            chapter_data: 章节数据，包含title, content, plan等
        """
        chapter_file = os.path.join(self.chapters_dir, f"chapter_{chapter_number:03d}.json")
        chapter_data['chapter_number'] = chapter_number
        chapter_data['created_at'] = datetime.now().isoformat()
        
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
    
    def load_chapter(self, chapter_number):
        """加载章节内容"""
        chapter_file = os.path.join(self.chapters_dir, f"chapter_{chapter_number:03d}.json")
        if os.path.exists(chapter_file):
            with open(chapter_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def get_all_chapters(self):
        """获取所有章节"""
        chapters = []
        if not os.path.exists(self.chapters_dir):
            return chapters
        
        for filename in sorted(os.listdir(self.chapters_dir)):
            if filename.startswith('chapter_') and filename.endswith('.json'):
                filepath = os.path.join(self.chapters_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    chapters.append(json.load(f))
        
        return chapters
    
    def get_latest_chapter_number(self):
        """获取最新章节编号"""
        chapters = self.get_all_chapters()
        if not chapters:
            return 0
        return max(ch.get('chapter_number', 0) for ch in chapters)
    
    def update_chapter(self, chapter_number, updates):
        """更新章节内容"""
        chapter_data = self.load_chapter(chapter_number)
        if chapter_data:
            chapter_data.update(updates)
            chapter_data['updated_at'] = datetime.now().isoformat()
            self.save_chapter(chapter_number, chapter_data)
            return True
        return False
    
    def get_all_content_text(self):
        """获取所有章节的文本内容（用于问答系统）"""
        chapters = self.get_all_chapters()
        texts = []
        for chapter in chapters:
            text = f"第{chapter['chapter_number']}章 {chapter.get('title', '')}\n\n{chapter.get('content', '')}"
            texts.append({
                'chapter_number': chapter['chapter_number'],
                'title': chapter.get('title', ''),
                'text': text
            })
        return texts
    
    # 悬疑推理小说专用存储方法
    
    def save_mystery_outline(self, outline_data):
        """保存悬疑推理小说大纲"""
        mystery_dir = os.path.join(os.path.dirname(self.outline_file), 'mystery')
        os.makedirs(mystery_dir, exist_ok=True)
        
        outline_file = os.path.join(mystery_dir, f"outline_{outline_data['id']}.json")
        with open(outline_file, 'w', encoding='utf-8') as f:
            json.dump(outline_data, f, ensure_ascii=False, indent=2)
    
    def load_mystery_outline(self, outline_id=None):
        """加载悬疑推理小说大纲"""
        mystery_dir = os.path.join(os.path.dirname(self.outline_file), 'mystery')
        
        if outline_id:
            outline_file = os.path.join(mystery_dir, f"outline_{outline_id}.json")
            if os.path.exists(outline_file):
                with open(outline_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        else:
            # 返回最新的大纲
            if os.path.exists(mystery_dir):
                files = [f for f in os.listdir(mystery_dir) if f.startswith('outline_')]
                if files:
                    latest_file = sorted(files)[-1]
                    with open(os.path.join(mystery_dir, latest_file), 'r', encoding='utf-8') as f:
                        return json.load(f)
        return None
    
    def save_clue_system(self, outline_id, clue_system_data):
        """保存线索系统"""
        mystery_dir = os.path.join(os.path.dirname(self.outline_file), 'mystery')
        clues_dir = os.path.join(mystery_dir, 'clues')
        os.makedirs(clues_dir, exist_ok=True)
        
        clue_file = os.path.join(clues_dir, f"clue_system_{outline_id}.json")
        with open(clue_file, 'w', encoding='utf-8') as f:
            json.dump(clue_system_data, f, ensure_ascii=False, indent=2)
    
    def load_clue_system(self, outline_id):
        """加载线索系统"""
        mystery_dir = os.path.join(os.path.dirname(self.outline_file), 'mystery')
        clue_file = os.path.join(mystery_dir, 'clues', f"clue_system_{outline_id}.json")
        
        if os.path.exists(clue_file):
            with open(clue_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_character_relationships(self, outline_id, relationships_data):
        """保存角色关系图"""
        mystery_dir = os.path.join(os.path.dirname(self.outline_file), 'mystery')
        chars_dir = os.path.join(mystery_dir, 'characters')
        os.makedirs(chars_dir, exist_ok=True)
        
        char_file = os.path.join(chars_dir, f"relationships_{outline_id}.json")
        with open(char_file, 'w', encoding='utf-8') as f:
            json.dump(relationships_data, f, ensure_ascii=False, indent=2)
    
    def load_character_relationships(self, outline_id):
        """加载角色关系图"""
        mystery_dir = os.path.join(os.path.dirname(self.outline_file), 'mystery')
        char_file = os.path.join(mystery_dir, 'characters', f"relationships_{outline_id}.json")
        
        if os.path.exists(char_file):
            with open(char_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_clue(self, clue_id, clue_data):
        """保存单个线索"""
        mystery_dir = os.path.join(os.path.dirname(self.outline_file), 'mystery')
        clues_dir = os.path.join(mystery_dir, 'individual_clues')
        os.makedirs(clues_dir, exist_ok=True)
        
        clue_file = os.path.join(clues_dir, f"clue_{clue_id}.json")
        with open(clue_file, 'w', encoding='utf-8') as f:
            json.dump(clue_data, f, ensure_ascii=False, indent=2)
    
    def load_clue(self, clue_id):
        """加载单个线索"""
        mystery_dir = os.path.join(os.path.dirname(self.outline_file), 'mystery')
        clue_file = os.path.join(mystery_dir, 'individual_clues', f"clue_{clue_id}.json")
        
        if os.path.exists(clue_file):
            with open(clue_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def get_all_clues(self):
        """获取所有线索"""
        mystery_dir = os.path.join(os.path.dirname(self.outline_file), 'mystery')
        clues_dir = os.path.join(mystery_dir, 'individual_clues')
        
        clues = []
        if os.path.exists(clues_dir):
            for filename in os.listdir(clues_dir):
                if filename.startswith('clue_') and filename.endswith('.json'):
                    filepath = os.path.join(clues_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        clues.append(json.load(f))
        
        return clues
    
    def save_tomato_optimized_chapter(self, chapter_number, chapter_data):
        """保存番茄小说优化的章节"""
        tomato_dir = os.path.join(self.chapters_dir, 'tomato_optimized')
        os.makedirs(tomato_dir, exist_ok=True)
        
        chapter_file = os.path.join(tomato_dir, f"chapter_{chapter_number:03d}.json")
        chapter_data['platform'] = 'tomato_novel'
        chapter_data['optimized_at'] = datetime.now().isoformat()
        
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
