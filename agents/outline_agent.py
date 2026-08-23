"""大纲Agent - 负责小说整体大纲构思"""
import json
import re
from utils import LLMClient, Storage, config
from .prompts import (
    OUTLINE_AGENT_SYSTEM_PROMPT,
    OUTLINE_AGENT_AUTONOMOUS_PROMPT,
    OUTLINE_AGENT_CUSTOMIZED_PROMPT_TEMPLATE
)

class OutlineAgent:
    """大纲Agent"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.storage = Storage()
    
    def create_outline(self, mode="autonomous", custom_settings=None):
        """
        创建小说大纲
        
        Args:
            mode: 创作模式，"autonomous"(自主构思) 或 "customized"(定制化)
            custom_settings: 定制化设置，包含genre, style, core_settings
        
        Returns:
            大纲数据（dict）
        """
        print("=" * 50)
        print("大纲Agent开始工作...")
        print("=" * 50)
        
        # 构建用户提示词
        if mode == "autonomous":
            user_prompt = OUTLINE_AGENT_AUTONOMOUS_PROMPT
        else:
            if not custom_settings:
                custom_settings = {
                    'genre': config.get('creation_mode.custom_settings.genre', ''),
                    'style': config.get('creation_mode.custom_settings.style', ''),
                    'core_settings': config.get('creation_mode.custom_settings.core_settings', '')
                }
            user_prompt = OUTLINE_AGENT_CUSTOMIZED_PROMPT_TEMPLATE.format(**custom_settings)
        
        # 调用LLM生成大纲（使用流式输出避免超时）
        print("\n正在生成小说大纲...")
        print("提示：使用流式输出，deepseek-r1会先思考再输出JSON...")

        messages = [
            {"role": "system", "content": OUTLINE_AGENT_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        response = self.llm.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=3000,
            stream=True  # 使用流式输出避免nginx超时
        )
        
        # 解析JSON响应
        outline_data = self._parse_outline_response(response)
        
        if outline_data:
            # 保存大纲
            self.storage.save_outline(outline_data)
            print("\n✓ 大纲生成完成并已保存")
            self._print_outline_summary(outline_data)
            return outline_data
        else:
            print("\n✗ 大纲解析失败")
            return None
    
    def _parse_outline_response(self, response):
        """解析LLM返回的大纲JSON（支持deepseek-r1的<think>标签和嵌套JSON）"""
        
        if not response or not response.strip():
            print("⚠️ 响应为空")
            return None

        # 策略0: 移除<think>标签内容（deepseek-r1特有）
        cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
        
        # 如果清理后为空，说明全部都是think标签
        if not cleaned_response:
            print("⚠️ 清理<think>标签后响应为空")
            return None

        # 策略1: 尝试直接解析清理后的响应
        try:
            data = json.loads(cleaned_response)
            if self._validate_outline_data(data):
                return data
        except json.JSONDecodeError:
            pass

        # 策略2: 提取```json代码块
        json_match = re.search(r'```json\s*(.*?)\s*```', cleaned_response, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1).strip())
                if self._validate_outline_data(data):
                    return data
            except json.JSONDecodeError:
                pass

        # 策略3: 提取```代码块（不带json标记）
        json_match = re.search(r'```\s*(.*?)\s*```', cleaned_response, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1).strip())
                if self._validate_outline_data(data):
                    return data
            except json.JSONDecodeError:
                pass

        # 策略4: 使用更强大的正则提取嵌套JSON（支持多层嵌套）
        json_candidates = self._extract_nested_json(cleaned_response)
        for json_str in json_candidates:
            try:
                data = json.loads(json_str)
                if self._validate_outline_data(data):
                    return data
            except json.JSONDecodeError:
                continue

        # 策略5: 尝试从原始响应中提取（最后备选）
        if cleaned_response != response:
            json_candidates = self._extract_nested_json(response)
            for json_str in json_candidates:
                try:
                    data = json.loads(json_str)
                    if self._validate_outline_data(data):
                        return data
                except json.JSONDecodeError:
                    continue

        # 所有策略都失败，打印调试信息
        print("\n⚠️  无法解析大纲JSON")
        print("原始响应长度:", len(response))
        print("清理后响应长度:", len(cleaned_response))
        print("原始响应前500字符：")
        print(response[:500])
        print("\n清理后响应前500字符：")
        print(cleaned_response[:500])
        if len(cleaned_response) > 500:
            print("\n清理后响应后500字符：")
            print(cleaned_response[-500:])
        return None
    
    def _validate_outline_data(self, data):
        """验证大纲数据是否有效"""
        if not isinstance(data, dict):
            return False
        
        # 检查必需字段
        required_fields = ['novel_title', 'genre', 'theme']
        return any(field in data for field in required_fields)

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
    
    def _print_outline_summary(self, outline):
        """打印大纲摘要"""
        print("\n" + "=" * 50)
        print("大纲摘要")
        print("=" * 50)
        print(f"标题: {outline.get('novel_title', 'N/A')}")
        print(f"题材: {outline.get('genre', 'N/A')}")
        print(f"主题: {outline.get('theme', 'N/A')}")
        print(f"章节数: {len(outline.get('chapter_outline', []))}")
        
        if 'main_characters' in outline:
            print(f"\n主要人物:")
            for char in outline['main_characters'][:3]:  # 只显示前3个
                if isinstance(char, dict):
                    print(f"  - {char.get('name', 'N/A')}: {char.get('role', 'N/A')}")
        
        print("=" * 50)
    
    def get_outline(self):
        """获取已保存的大纲"""
        return self.storage.load_outline()
    
    def update_outline(self, updates):
        """更新大纲"""
        outline = self.get_outline()
        if outline:
            outline.update(updates)
            self.storage.save_outline(outline)
            return True
        return False
