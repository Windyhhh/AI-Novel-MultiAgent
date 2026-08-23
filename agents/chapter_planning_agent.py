"""章节规划Agent - 负责章节内容规划"""
import json
import re
from utils import LLMClient, Storage, config
from .prompts import (
    CHAPTER_PLANNING_AGENT_SYSTEM_PROMPT,
    CHAPTER_PLANNING_AGENT_PROMPT_TEMPLATE
)

class ChapterPlanningAgent:
    """章节规划Agent"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.storage = Storage()
    
    def plan_chapter(self, chapter_number, outline=None):
        """
        规划指定章节
        
        Args:
            chapter_number: 章节编号
            outline: 小说大纲（如果为None则从存储加载）
        
        Returns:
            章节规划数据（dict）
        """
        print("=" * 50)
        print(f"章节规划Agent开始规划第{chapter_number}章...")
        print("=" * 50)
        
        # 加载大纲
        if outline is None:
            outline = self.storage.load_outline()
        
        if not outline:
            print("✗ 未找到小说大纲，请先创建大纲")
            return None
        
        # 获取章节大纲信息
        chapter_outline_info = self._get_chapter_outline_info(outline, chapter_number)
        if not chapter_outline_info:
            print(f"✗ 大纲中未找到第{chapter_number}章的信息")
            return None
        
        # 获取前情提要
        previous_summary = self._get_previous_summary(chapter_number)
        
        # 确定故事阶段
        total_chapters = len(outline.get('chapter_outline', []))
        story_phase = self._determine_story_phase(chapter_number, total_chapters)
        
        # 获取目标字数
        target_word_count = config.get('chapter.default_length', 3000)
        
        # 构建提示词
        user_prompt = CHAPTER_PLANNING_AGENT_PROMPT_TEMPLATE.format(
            chapter_number=chapter_number,
            novel_title=outline.get('novel_title', ''),
            total_chapters=total_chapters,
            story_phase=story_phase,
            chapter_outline_info=chapter_outline_info,
            previous_summary=previous_summary,
            target_word_count=target_word_count
        )
        
        # 调用LLM生成规划（使用流式输出避免超时）
        print(f"\n正在规划第{chapter_number}章...")

        messages = [
            {"role": "system", "content": CHAPTER_PLANNING_AGENT_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        response = self.llm.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            stream=True  # 使用流式输出避免超时
        )
        
        # 解析JSON响应
        plan_data = self._parse_plan_response(response)
        
        if plan_data:
            print(f"\n✓ 第{chapter_number}章规划完成")
            self._print_plan_summary(plan_data)
            return plan_data
        else:
            print(f"\n✗ 第{chapter_number}章规划解析失败")
            return None
    
    def _get_chapter_outline_info(self, outline, chapter_number):
        """获取章节在大纲中的信息"""
        chapter_outline = outline.get('chapter_outline', [])
        if chapter_number <= len(chapter_outline):
            chapter_info = chapter_outline[chapter_number - 1]
            if isinstance(chapter_info, dict):
                return json.dumps(chapter_info, ensure_ascii=False, indent=2)
            else:
                return str(chapter_info)
        return None
    
    def _get_previous_summary(self, chapter_number):
        """获取前情提要"""
        if chapter_number == 1:
            return "这是第一章，没有前情。"
        
        # 获取前一章的内容
        prev_chapter = self.storage.load_chapter(chapter_number - 1)
        if prev_chapter:
            content = prev_chapter.get('content', '')
            # 简单截取前200字作为提要
            summary = content[:200] + "..." if len(content) > 200 else content
            return f"前一章概要：{summary}"
        
        return "前情未知。"
    
    def _determine_story_phase(self, chapter_number, total_chapters):
        """确定故事阶段"""
        progress = chapter_number / total_chapters
        if progress <= 0.25:
            return "开篇阶段（引入世界观、人物、初始冲突）"
        elif progress <= 0.5:
            return "发展阶段（冲突升级、人物成长）"
        elif progress <= 0.75:
            return "高潮阶段（主要冲突爆发）"
        else:
            return "收尾阶段（解决冲突、故事收束）"
    
    def _parse_plan_response(self, response):
        """解析LLM返回的规划JSON（支持deepseek-r1的<think>标签和嵌套JSON）"""

        # 策略0: 移除<think>标签内容
        cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()

        # 策略1: 尝试直接解析清理后的响应
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            pass

        # 策略2: 尝试直接解析原始响应
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # 策略3: 提取```json代码块
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # 策略4: 提取```代码块（不带json标记）
        json_match = re.search(r'```\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # 策略5: 使用更强大的方法提取嵌套JSON
        json_candidates = self._extract_nested_json(cleaned_response)
        for json_str in json_candidates:
            try:
                data = json.loads(json_str)
                if 'chapter_title' in data or 'title' in data:
                    return data
            except json.JSONDecodeError:
                continue

        # 策略6: 从原始响应中提取
        json_candidates = self._extract_nested_json(response)
        for json_str in json_candidates:
            try:
                data = json.loads(json_str)
                if 'chapter_title' in data or 'title' in data:
                    return data
            except json.JSONDecodeError:
                continue

        print("\n⚠️  无法解析规划JSON")
        print("原始响应前500字符：")
        print(response[:500])
        print("\n原始响应后500字符：")
        print(response[-500:])
        return None

    def _extract_nested_json(self, text):
        """提取文本中所有可能的JSON对象（支持嵌套）"""
        candidates = []
        depth = 0
        start = -1

        for i, char in enumerate(text):
            if char == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0 and start != -1:
                    candidates.append(text[start:i+1])
                    start = -1

        # 从最长的开始尝试（通常最完整）
        return sorted(candidates, key=len, reverse=True)
    
    def _print_plan_summary(self, plan):
        """打印规划摘要"""
        print("\n" + "-" * 50)
        print(f"章节标题: {plan.get('chapter_title', 'N/A')}")
        print(f"目标字数: {plan.get('word_count', 'N/A')}")
        print(f"情感基调: {plan.get('emotional_tone', 'N/A')}")
        print("-" * 50)

