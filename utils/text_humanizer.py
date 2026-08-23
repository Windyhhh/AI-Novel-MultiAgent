"""
文本人性化处理器
专门消除AI痕迹，让文本更加自然人性化
"""

import re
import json
from typing import Dict, List, Any, Tuple
from utils import LLMClient, get_logger

logger = get_logger('text_humanizer')

class TextHumanizer:
    """文本人性化处理器"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        
        # AI痕迹替换规则
        self.ai_replacements = {
            r'深深地感受到': ['感受到', '体会到', '意识到'],
            r'静静地思考': ['思考着', '想着', '琢磨着'],
            r'慢慢地走': ['走着', '踱步', '迈步'],
            r'然而却': ['不过', '但是', '可是'],
            r'仿佛感觉': ['感觉', '觉得', '像是'],
            r'在.*?的阳光下': ['阳光中', '阳光里', '日光下'],
            r'眼中闪过一丝': ['眼神', '目光中透着', '眼里带着'],
            r'心中划过一抹': ['心里', '内心', '心头'],
        }
        
        # 情感表达增强词库
        self.emotion_enhancements = {
            '高兴': ['欣喜', '愉悦', '开心', '兴奋', '雀跃'],
            '伤心': ['难过', '痛苦', '心酸', '哀伤', '悲痛'],
            '愤怒': ['气愤', '恼怒', '暴怒', '火冒三丈', '怒不可遏'],
            '害怕': ['恐惧', '惊恐', '胆怯', '心惊胆战', '毛骨悚然'],
            '惊讶': ['震惊', '吃惊', '诧异', '目瞪口呆', '瞠目结舌']
        }
    
    def humanize(self, content: str, aggressive: bool = False) -> Dict[str, Any]:
        """人性化文本"""
        try:
            humanized_text = content
            
            # 第一步：去除AI痕迹
            humanized_text = self._remove_ai_patterns(humanized_text)
            
            # 第二步：增强情感表达
            humanized_text = self._enhance_emotions(humanized_text)
            
            # 第三步：优化对话
            humanized_text = self._naturalize_dialogue(humanized_text)
            
            # 第四步：调整叙事节奏
            humanized_text = self._adjust_rhythm(humanized_text)
            
            if aggressive:
                # 激进模式：使用LLM进一步优化
                humanized_text = self._deep_humanize(humanized_text)
            
            return {
                'success': True,
                'humanized_text': humanized_text,
                'improvements': self._analyze_improvements(content, humanized_text)
            }
            
        except Exception as e:
            logger.error(f"文本人性化处理失败: {e}")
            return {
                'success': False,
                'humanized_text': content,
                'error': str(e)
            }
    
    def _remove_ai_patterns(self, text: str) -> str:
        """去除AI痕迹"""
        result = text
        
        for pattern, replacements in self.ai_replacements.items():
            matches = re.findall(pattern, result)
            for match in matches:
                # 随机选择替换词
                import random
                replacement = random.choice(replacements)
                result = result.replace(match, replacement, 1)
        
        return result
    
    def _enhance_emotions(self, text: str) -> str:
        """增强情感表达"""
        result = text
        
        for basic_emotion, enhanced_list in self.emotion_enhancements.items():
            if basic_emotion in result:
                import random
                enhanced = random.choice(enhanced_list)
                # 不是完全替换，而是在某些情况下替换
                if result.count(basic_emotion) > 2:
                    result = result.replace(basic_emotion, enhanced, 1)
        
        return result
    
    def _naturalize_dialogue(self, text: str) -> str:
        """自然化对话"""
        # 查找对话部分
        dialogues = re.findall(r'"([^"]*)"', text)
        
        for dialogue in dialogues:
            if len(dialogue) > 10:  # 只处理较长的对话
                # 添加语气词、口语化表达
                naturalized = self._add_conversational_elements(dialogue)
                text = text.replace(f'"{dialogue}"', f'"{naturalized}"', 1)
        
        return text
    
    def _add_conversational_elements(self, dialogue: str) -> str:
        """添加对话元素"""
        # 简单的口语化处理
        conversational_markers = ['啊', '呢', '吧', '嘛', '呀']
        
        # 在句末适当添加语气词
        if dialogue.endswith('。') or dialogue.endswith('.'):
            import random
            if random.random() < 0.3:  # 30%概率添加
                marker = random.choice(conversational_markers)
                dialogue = dialogue[:-1] + marker + '。'
        
        return dialogue
    
    def _adjust_rhythm(self, text: str) -> str:
        """调整叙事节奏"""
        # 检测过长的句子并分割
        sentences = re.split(r'[。！？]', text)
        adjusted_sentences = []
        
        for sentence in sentences:
            if len(sentence) > 80:  # 过长句子
                # 尝试在合适位置分割
                split_points = ['，', '、', '；']
                for point in split_points:
                    if point in sentence:
                        parts = sentence.split(point, 1)
                        if len(parts[0]) > 20 and len(parts[1]) > 20:
                            sentence = parts[0] + '。' + parts[1]
                            break
            
            adjusted_sentences.append(sentence)
        
        return '。'.join(adjusted_sentences)
    
    def _deep_humanize(self, text: str) -> str:
        """深度人性化（使用LLM）"""
        prompt = f"""
请将以下AI生成的文本进行深度人性化处理，消除所有AI痕迹：

原文：
{text}

人性化要求：
1. 语言自然流畅，避免程式化表达
2. 情感真实细腻，有温度感
3. 对话生动有个性，符合角色特点
4. 描写具体生动，避免空洞华丽
5. 节奏张弛有度，突出重点
6. 完全消除"深深地"、"静静地"等AI痕迹
7. 保持原文长度和主要内容不变

请输出人性化后的文本：
"""
        
        try:
            return self.llm.generate(prompt, max_tokens=4000, temperature=0.7)
        except Exception as e:
            logger.error(f"深度人性化失败: {e}")
            return text
    
    def _analyze_improvements(self, original: str, humanized: str) -> List[str]:
        """分析改进点"""
        improvements = []
        
        # 检查AI痕迹减少
        ai_patterns = [r'深深地', r'静静地', r'慢慢地', r'然而却', r'仿佛感觉']
        for pattern in ai_patterns:
            original_count = len(re.findall(pattern, original))
            humanized_count = len(re.findall(pattern, humanized))
            if humanized_count < original_count:
                improvements.append(f'减少AI痕迹"{pattern}"')
        
        # 检查情感词汇增强
        if '欣喜' in humanized and '高兴' in original:
            improvements.append('增强情感表达')
        
        # 检查对话优化
        original_dialogues = len(re.findall(r'"[^"]*"', original))
        humanized_dialogues = len(re.findall(r'"[^"]*[啊呢吧嘛呀][^"]*"', humanized))
        if humanized_dialogues > 0:
            improvements.append('自然化对话')
        
        return improvements
