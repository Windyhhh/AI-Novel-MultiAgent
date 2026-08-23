"""
内容质量分析器
专门检测和分析AI小说中的质量问题
"""

import re
import json
from typing import Dict, List, Any
from utils import get_logger

logger = get_logger('quality_analyzer')

class QualityAnalyzer:
    """内容质量分析器"""
    
    def __init__(self):
        # AI痕迹检测模式
        self.ai_patterns = [
            r'(然而|但是|不过).*?(却|确)',
            r'(深深地|静静地|慢慢地).*?(感受|思考|观察)',
            r'(仿佛|似乎|好像).*?(感觉|觉得)',
            r'在.*?的(阳光|月光|灯光)下',
            r'(眼中|心中).*?(闪过|划过).*?(一丝|一抹)',
        ]
        
        # 套路化表达检测
        self.cliche_patterns = [
            r'冷笑.*?(眯|眼)',
            r'霸道.*?(总裁|CEO)',
            r'(完美|绝色).*?(容颜|面容)',
            r'(心如|宛如).*?(刀绞|止水)',
        ]
    
    def analyze(self, content: str) -> Dict[str, Any]:
        """全面分析内容质量"""
        # 先进行各项分析
        ai_patterns = self._detect_ai_patterns(content)
        emotional_depth = self._analyze_emotional_depth(content)
        character_depth = self._analyze_character_depth(content)
        narrative_rhythm = self._analyze_narrative_rhythm(content)
        language_quality = self._analyze_language_quality(content)
        originality = self._analyze_originality(content)
        cultural_authenticity = self._analyze_cultural_authenticity(content)
        
        # 计算总体分数
        overall_score = self._calculate_overall_score_from_components(
            ai_patterns, emotional_depth, character_depth, narrative_rhythm,
            language_quality, originality, cultural_authenticity
        )
        
        return {
            'overall_score': overall_score,
            'ai_patterns': ai_patterns,
            'emotional_depth': emotional_depth,
            'character_depth': character_depth,
            'narrative_rhythm': narrative_rhythm,
            'language_quality': language_quality,
            'originality': originality,
            'cultural_authenticity': cultural_authenticity
        }
    
    def _detect_ai_patterns(self, content: str) -> Dict[str, Any]:
        """检测AI痕迹"""
        ai_count = 0
        detected_patterns = []
        
        for pattern in self.ai_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                ai_count += len(matches)
                detected_patterns.extend(matches)
        
        # 检测套路化表达
        cliche_count = 0
        for pattern in self.cliche_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            cliche_count += len(matches)
        
        total_sentences = len(re.split(r'[.!?。！？]', content))
        ai_ratio = (ai_count + cliche_count) / max(total_sentences, 1)
        
        return {
            'ai_score': max(0, 10 - ai_ratio * 100),  # 0-10分，越高越好
            'human_score': min(10, ai_ratio * 100),   # 人性化程度
            'detected_patterns': detected_patterns[:5],  # 前5个检测到的问题
            'ai_count': ai_count,
            'cliche_count': cliche_count
        }
    
    def _analyze_emotional_depth(self, content: str) -> Dict[str, Any]:
        """分析情感深度"""
        # 检测情感词汇丰富度
        emotion_words = [
            '愤怒', '悲伤', '喜悦', '恐惧', '惊讶', '厌恶', '羞愧', '内疚',
            '嫉妒', '骄傲', '感激', '同情', '怜悯', '敬畏', '困惑', '焦虑'
        ]
        
        emotion_count = 0
        for word in emotion_words:
            emotion_count += content.count(word)
        
        # 检测情感描写层次
        complex_emotions = [
            '复杂', '矛盾', '纠结', '挣扎', '五味杂陈', '百感交集'
        ]
        
        complex_count = sum(content.count(word) for word in complex_emotions)
        
        return {
            'depth_score': min(10, (emotion_count + complex_count * 2) / 5),
            'emotion_variety': len([word for word in emotion_words if word in content]),
            'complexity_level': complex_count
        }
    
    def _analyze_character_depth(self, content: str) -> Dict[str, Any]:
        """分析人物塑造深度"""
        # 检测人物描写维度
        physical_desc = len(re.findall(r'(长相|容貌|身材|外表)', content))
        psychological_desc = len(re.findall(r'(性格|心理|内心|想法)', content))
        behavioral_desc = len(re.findall(r'(行为|动作|举止|习惯)', content))
        
        # 检测对话个性化
        dialogue_count = len(re.findall(r'"[^"]*"', content))
        unique_phrases = len(re.findall(r'(口头禅|习惯|怪癖)', content))
        
        depth_score = (psychological_desc * 3 + behavioral_desc * 2 + physical_desc) / 10
        
        return {
            'depth_score': min(10, depth_score),
            'dimensions': {
                'physical': physical_desc,
                'psychological': psychological_desc, 
                'behavioral': behavioral_desc
            },
            'dialogue_personality': min(10, unique_phrases * 2),
            'dialogue_count': dialogue_count
        }
    
    def _analyze_narrative_rhythm(self, content: str) -> Dict[str, Any]:
        """分析叙事节奏"""
        sentences = re.split(r'[.!?。！？]', content)
        sentence_lengths = [len(s.strip()) for s in sentences if s.strip()]
        
        if not sentence_lengths:
            return {'rhythm_score': 0}
        
        # 计算句子长度方差（衡量节奏变化）
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((length - avg_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
        
        # 检测节奏控制词汇
        rhythm_words = ['突然', '慢慢', '瞬间', '逐渐', '猛然', '静静']
        rhythm_control = sum(content.count(word) for word in rhythm_words)
        
        rhythm_score = min(10, (variance / 100) + rhythm_control / 5)
        
        return {
            'rhythm_score': rhythm_score,
            'sentence_variety': variance,
            'rhythm_control': rhythm_control,
            'avg_sentence_length': avg_length
        }
    
    def _analyze_language_quality(self, content: str) -> Dict[str, Any]:
        """分析语言质量"""
        # 检测重复词汇
        words = re.findall(r'[\u4e00-\u9fff]+', content)
        word_freq = {}
        for word in words:
            if len(word) > 1:  # 忽略单字
                word_freq[word] = word_freq.get(word, 0) + 1
        
        repetition_ratio = sum(1 for count in word_freq.values() if count > 3) / len(word_freq) if word_freq else 0
        
        # 检测修辞手法
        rhetoric_patterns = [
            r'如.*?一般', r'仿佛.*?一样', r'像.*?似的',  # 比喻
            r'.*?的.*?，.*?的.*?', # 排比
            r'难道.*?吗', # 反问
        ]
        
        rhetoric_count = sum(len(re.findall(pattern, content)) for pattern in rhetoric_patterns)
        
        return {
            'quality_score': min(10, 10 - repetition_ratio * 5 + rhetoric_count / 5),
            'repetition_ratio': repetition_ratio,
            'rhetoric_usage': rhetoric_count,
            'vocabulary_richness': len(set(words)) / len(words) if words else 0
        }
    
    def _analyze_originality(self, content: str) -> Dict[str, Any]:
        """分析原创性"""
        # 检测常见套路
        common_plots = [
            '灰姑娘', '霸道总裁', '穿越重生', '系统流', '废材逆袭',
            '三角恋', '替身文', '豪门恩怨', '校园霸凌'
        ]
        
        plot_cliches = sum(content.count(plot) for plot in common_plots)
        
        # 检测创新元素
        innovation_words = [
            '独特', '创新', '突破', '颠覆', '前所未有', '与众不同'
        ]
        
        innovation_signals = sum(content.count(word) for word in innovation_words)
        
        return {
            'originality_score': min(10, 10 - plot_cliches + innovation_signals),
            'cliche_count': plot_cliches,
            'innovation_signals': innovation_signals
        }
    
    def _analyze_cultural_authenticity(self, content: str) -> Dict[str, Any]:
        """分析文化真实性"""
        # 检测文化元素
        cultural_elements = [
            '方言', '习俗', '传统', '节日', '风土', '人情', '礼仪'
        ]
        
        cultural_count = sum(content.count(element) for element in cultural_elements)
        
        # 检测地域特色
        regional_words = [
            '胡同', '弄堂', '巷子', '茶馆', '酒楼', '当铺'
        ]
        
        regional_count = sum(content.count(word) for word in regional_words)
        
        return {
            'authenticity_score': min(10, (cultural_count + regional_count) / 2),
            'cultural_elements': cultural_count,
            'regional_features': regional_count
        }
    
    def _calculate_overall_score_from_components(self, ai_patterns: Dict, emotional_depth: Dict,
                                                character_depth: Dict, narrative_rhythm: Dict,
                                                language_quality: Dict, originality: Dict,
                                                cultural_authenticity: Dict) -> float:
        """从各个组件计算总体质量分数"""
        # 加权计算总分
        scores = {
            'ai_patterns': ai_patterns.get('ai_score', 0),
            'emotional_depth': emotional_depth.get('depth_score', 0),
            'character_depth': character_depth.get('depth_score', 0),
            'narrative_rhythm': narrative_rhythm.get('rhythm_score', 0),
            'language_quality': language_quality.get('quality_score', 0),
            'originality': originality.get('originality_score', 0),
            'cultural_authenticity': cultural_authenticity.get('authenticity_score', 0)
        }
        
        weights = {
            'ai_patterns': 0.2,
            'emotional_depth': 0.15,
            'character_depth': 0.15,
            'narrative_rhythm': 0.15,
            'language_quality': 0.15,
            'originality': 0.1,
            'cultural_authenticity': 0.1
        }
        
        total_score = sum(scores[aspect] * weights[aspect] for aspect in scores.keys())
        
        return round(total_score, 2)
