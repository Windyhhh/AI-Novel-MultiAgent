"""
番茄小说平台特化智能体
针对番茄小说平台的特点优化内容生成
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from utils import LLMClient, get_logger, Storage

logger = get_logger('tomato_novel_agent')

class TomatoNovelAgent:
    """番茄小说平台特化智能体"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.storage = Storage()
        
        # 番茄小说平台特点
        self.platform_features = {
            'chapter_length': {'min': 2000, 'ideal': 2500, 'max': 3500},
            'hook_frequency': 'every_chapter',  # 每章都要有悬念点
            'pace': 'fast',  # 快节奏
            'reader_retention': {
                'first_3_chapters': '必须抓住读者',
                'chapter_endings': '必须有悬念',
                'plot_points': '每10章一个爽点'
            }
        }
    
    def generate_mystery_chapter(self, chapter_plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """生成悬疑推理章节（针对番茄小说平台优化）"""
        chapter_number = chapter_plan.get('chapter_number', 1)
        clue_system = context.get('clue_system', {})
        character_relationships = context.get('character_relationships', {})
        
        # 获取本章应该揭示的线索
        chapter_clues = self._get_chapter_clues(chapter_number, clue_system)
        
        # 构建番茄小说风格的提示词
        prompt = f"""
作为番茄小说平台的悬疑推理专家，请生成第{chapter_number}章内容。

## 平台要求
- 字数：2200-2800字（适合番茄小说）
- 节奏：快速推进，每页都要有看点
- 悬念：章末必须留悬念，让读者想看下一章
- 语言：简洁明快，适合手机阅读
- 爽点：要有让读者兴奋的情节点

## 章节规划
{json.dumps(chapter_plan, ensure_ascii=False, indent=2)}

## 线索布局
本章需要处理的线索：
{json.dumps(chapter_clues, ensure_ascii=False, indent=2)}

## 角色关系
{json.dumps(character_relationships.get('raw_relationships', ''), ensure_ascii=False)}

## 写作要求
1. **开头抓人**：前200字必须有强烈的吸引力
2. **节奏控制**：
   - 每500字一个小转折
   - 每1000字一个情节推进
   - 章末留一个悬念点
3. **对话生动**：多用对话推进剧情，增加现场感
4. **细节描写**：关键线索的发现要有详细描述
5. **情绪渲染**：营造悬疑氛围，但不要过度阴暗

## 番茄小说特色元素
- 适当的"反转"让读者惊喜
- 主角要有"高光时刻"体现能力
- 线索发现要有"推理快感"
- 章末要有"想知道后续"的冲动

请生成完整的章节内容，确保符合推理逻辑，同时具有网文的可读性和吸引力。
"""
        
        try:
            # 生成初始内容
            response = self.llm.generate(prompt, max_tokens=3500, temperature=0.8)
            
            # 优化章节结构
            optimized_content = self._optimize_for_tomato(response, chapter_number)
            
            # 添加悬念点检查
            suspense_check = self._check_suspense_points(optimized_content)
            
            # 字数检查和调整
            word_count = len(optimized_content)
            if word_count < 2200:
                optimized_content = self._expand_content(optimized_content, chapter_plan)
            elif word_count > 3500:
                optimized_content = self._compress_content(optimized_content)
            
            result = {
                'chapter_number': chapter_number,
                'content': optimized_content,
                'word_count': len(optimized_content),
                'platform_optimized': True,
                'suspense_points': suspense_check.get('suspense_points', []),
                'tomato_score': self._calculate_tomato_score(optimized_content),
                'clues_revealed': chapter_clues,
                'generated_at': datetime.now().isoformat()
            }
            
            logger.info(f"生成番茄小说第{chapter_number}章，字数: {word_count}")
            return result
            
        except Exception as e:
            logger.error(f"生成番茄小说章节失败: {e}")
            return None
    
    def optimize_chapter_for_retention(self, chapter_content: str, chapter_number: int) -> Dict[str, Any]:
        """优化章节以提高读者留存率"""
        prompt = f"""
作为番茄小说编辑专家，请优化以下第{chapter_number}章内容，提高读者留存率：

原始内容：
{chapter_content}

优化要求：
1. **开头优化**：如果开头不够抓人，请重写开头200字
2. **节奏优化**：确保每500-800字有一个小高潮或转折
3. **悬念优化**：章末必须有强烈的悬念点
4. **对话优化**：增加生动对话，减少大段描述
5. **情绪优化**：在关键情节点增强情绪渲染

## 番茄小说留存技巧
- 前3章：必须有强烈冲突和悬念
- 每章结尾：用"突然"、"这时"、"没想到"等营造悬念
- 信息控制：每章揭示一点真相，但留下更大疑问
- 角色魅力：让主角在推理过程中展现魅力

请输出优化后的完整章节内容，并说明主要改动点。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=4000, temperature=0.7)
            
            # 分离改动说明和优化内容
            parts = response.split('主要改动点：')
            optimized_content = parts[0].strip()
            improvements = parts[1].strip() if len(parts) > 1 else "未提供改动说明"
            
            return {
                'optimized_content': optimized_content,
                'improvements': improvements,
                'retention_score': self._calculate_retention_score(optimized_content),
                'word_count': len(optimized_content)
            }
            
        except Exception as e:
            logger.error(f"优化章节留存率失败: {e}")
            return {'optimized_content': chapter_content, 'improvements': '优化失败'}
    
    def generate_cliffhanger_endings(self, chapter_content: str, next_chapter_plan: Dict[str, Any] = None) -> List[str]:
        """生成悬念结尾选项"""
        prompt = f"""
基于以下章节内容，生成5个不同风格的悬念结尾选项：

章节内容：
{chapter_content}

下章预告（如果有）：
{json.dumps(next_chapter_plan, ensure_ascii=False) if next_chapter_plan else "无"}

请生成5种悬念结尾风格：
1. **疑问式**：抛出一个关键疑问让读者思考
2. **转折式**：突然的情节转折
3. **发现式**：发现重要线索或证据
4. **危机式**：主角面临新的危险或困境
5. **揭示式**：揭示一个小真相但引出更大疑问

每个结尾控制在100-200字，要有强烈的"想知道下一章"的吸引力。
"""
        
        try:
            response = self.llm.generate(prompt, max_tokens=2000, temperature=0.9)
            
            # 解析不同的结尾选项
            endings = self._parse_ending_options(response)
            
            return endings
            
        except Exception as e:
            logger.error(f"生成悬念结尾失败: {e}")
            return [chapter_content[-200:]]  # 返回原结尾作为备选
    
    def _get_chapter_clues(self, chapter_number: int, clue_system: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取本章应该揭示的线索"""
        if not clue_system:
            return []
        
        # 根据章节号确定应该出现的线索
        chapter_clues = []
        
        # 早期章节 (1-20): 基础线索
        if 1 <= chapter_number <= 20:
            clue_types = ['physical_evidence', 'witness_testimony']
        # 中期章节 (21-40): 深入线索
        elif 21 <= chapter_number <= 40:
            clue_types = ['psychological_evidence', 'hidden_connections']
        # 后期章节 (41+): 关键线索
        else:
            clue_types = ['key_evidence', 'final_clues']
        
        return chapter_clues
    
    def _optimize_for_tomato(self, content: str, chapter_number: int) -> str:
        """针对番茄小说平台优化内容"""
        # 检查章节长度
        if len(content) < 2200:
            # 内容太短，需要扩展
            expansion_prompt = f"""
请将以下章节内容扩展至2500字左右，保持推理逻辑和番茄小说风格：

{content}

扩展要求：
1. 增加细节描写，特别是推理过程
2. 丰富对话内容，展现角色性格
3. 加强悬疑氛围营造
4. 确保新增内容与原文自然衔接
"""
            try:
                expanded = self.llm.generate(expansion_prompt, max_tokens=3000, temperature=0.7)
                return expanded
            except:
                return content
        
        return content
    
    def _check_suspense_points(self, content: str) -> Dict[str, Any]:
        """检查悬念点设置"""
        # 分析内容中的悬念点
        lines = content.split('\n')
        suspense_points = []
        
        # 简单的悬念点识别（可以用更复杂的NLP方法）
        suspense_keywords = ['突然', '这时', '没想到', '竟然', '意外', '发现', '？', '！']
        
        for i, line in enumerate(lines):
            for keyword in suspense_keywords:
                if keyword in line:
                    suspense_points.append({
                        'line_number': i + 1,
                        'content': line.strip(),
                        'type': keyword
                    })
        
        return {
            'suspense_points': suspense_points,
            'count': len(suspense_points),
            'quality': 'good' if len(suspense_points) >= 3 else 'needs_improvement'
        }
    
    def _calculate_tomato_score(self, content: str) -> float:
        """计算番茄小说适应度评分"""
        score = 0.0
        
        # 字数检查 (30%)
        word_count = len(content)
        if 2200 <= word_count <= 3000:
            score += 30.0
        elif 2000 <= word_count <= 3500:
            score += 20.0
        else:
            score += 10.0
        
        # 对话比例 (20%)
        dialogue_count = content.count('"') + content.count('"') + content.count('"')
        if dialogue_count >= 20:  # 充足对话
            score += 20.0
        elif dialogue_count >= 10:
            score += 15.0
        else:
            score += 5.0
        
        # 悬念词汇 (25%)
        suspense_keywords = ['突然', '这时', '没想到', '竟然', '意外', '发现']
        suspense_count = sum(content.count(word) for word in suspense_keywords)
        if suspense_count >= 5:
            score += 25.0
        elif suspense_count >= 3:
            score += 20.0
        else:
            score += 10.0
        
        # 段落结构 (25%)
        paragraphs = content.split('\n\n')
        avg_paragraph_length = sum(len(p) for p in paragraphs) / len(paragraphs)
        if 100 <= avg_paragraph_length <= 300:  # 适合手机阅读
            score += 25.0
        else:
            score += 15.0
        
        return min(100.0, score)
    
    def _calculate_retention_score(self, content: str) -> float:
        """计算读者留存评分"""
        score = 0.0
        
        # 开头吸引力
        opening = content[:200]
        if any(word in opening for word in ['死', '血', '尖叫', '发现', '突然']):
            score += 25.0
        
        # 章末悬念
        ending = content[-200:]
        if '？' in ending or '！' in ending or any(word in ending for word in ['下一章', '未完', '突然']):
            score += 25.0
        
        # 节奏控制
        content_parts = [content[i:i+1000] for i in range(0, len(content), 1000)]
        plot_points = 0
        for part in content_parts:
            if any(word in part for word in ['发现', '意外', '竟然', '没想到']):
                plot_points += 1
        
        if plot_points >= len(content_parts) * 0.7:  # 70%的部分有情节点
            score += 30.0
        
        # 对话活跃度
        dialogue_lines = content.count('\n') - content.replace('"', '').replace('"', '').replace('"', '').count('\n')
        if dialogue_lines >= 10:
            score += 20.0
        
        return min(100.0, score)
    
    def _expand_content(self, content: str, chapter_plan: Dict[str, Any]) -> str:
        """扩展章节内容到合适长度"""
        expansion_prompt = f"""
请将以下章节内容扩展，目标字数2500字，保持推理逻辑和番茄小说风格：

当前内容：
{content}

章节计划：
{json.dumps(chapter_plan, ensure_ascii=False)}

扩展方向：
1. 增加细节描写和环境渲染
2. 丰富角色对话和心理活动
3. 加强推理过程的展示
4. 增加悬疑氛围营造
"""
        
        try:
            return self.llm.generate(expansion_prompt, max_tokens=3000, temperature=0.7)
        except:
            return content
    
    def _compress_content(self, content: str) -> str:
        """压缩章节内容到合适长度"""
        compression_prompt = f"""
请将以下章节内容压缩到3000字以内，保持核心情节和推理逻辑：

{content}

压缩要求：
1. 保留所有关键情节点和线索
2. 保持悬念点和爽点
3. 精简描述，突出对话
4. 确保逻辑完整性
"""
        
        try:
            return self.llm.generate(compression_prompt, max_tokens=3500, temperature=0.5)
        except:
            return content[:3000]  # 简单截断作为备选
    
    def _parse_ending_options(self, response: str) -> List[str]:
        """解析悬念结尾选项"""
        endings = []
        lines = response.split('\n')
        current_ending = ""
        
        for line in lines:
            if any(line.startswith(f"{i}.") for i in range(1, 6)):
                if current_ending:
                    endings.append(current_ending.strip())
                current_ending = line
            elif current_ending:
                current_ending += " " + line
        
        if current_ending:
            endings.append(current_ending.strip())
        
        return endings[:5]  # 返回最多5个选项

class TomatoOptimizer:
    """番茄小说优化器"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def optimize_for_mobile_reading(self, content: str) -> str:
        """优化手机阅读体验"""
        prompt = f"""
请优化以下内容的手机阅读体验：

{content}

优化要求：
1. 段落不超过5行
2. 句子长度适中，避免过长句子
3. 增加换行和段落间隔
4. 对话独立成行
5. 重要信息突出显示

保持内容完整性和推理逻辑。
"""
        
        try:
            return self.llm.generate(prompt, max_tokens=len(content) + 500, temperature=0.5)
        except:
            return content
    
    def add_reader_engagement_elements(self, content: str) -> str:
        """添加读者互动元素"""
        # 在合适位置添加读者思考点
        # 例如："读者朋友们，你们觉得凶手会是谁呢？"
        # 这个功能可以根据番茄小说的具体要求来实现
        return content
