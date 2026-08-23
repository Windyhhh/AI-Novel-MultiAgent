"""
动态学习引擎
专门解决AI小说创作的8大核心问题，并能动态学习爆款小说特点
"""

import json
import re
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from utils import LLMClient, get_logger

logger = get_logger('dynamic_learning_engine')

class DynamicLearningEngine:
    """动态学习引擎 - 解决AI小说8大核心问题"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.bestseller_patterns = {}  # 爆款小说模式库
        self.genre_templates = {}      # 分类型模板库
        self.quality_standards = {}    # 质量标准库
        
        # 8大核心问题解决方案
        self.problem_solvers = {
            1: self._solve_logic_coherence,      # 逻辑连贯性
            2: self._solve_emotional_resonance,  # 情感共鸣
            3: self._solve_originality,          # 原创性
            4: self._solve_character_depth,      # 人物塑造
            5: self._solve_ai_language,          # AI语言问题
            6: self._solve_narrative_rhythm,     # 叙事节奏
            7: self._solve_theme_depth,          # 主题深度
            8: self._solve_cultural_authenticity # 文化适配
        }
        
        # 初始化学习数据库
        self._initialize_learning_database()
    
    def _initialize_learning_database(self):
        """初始化学习数据库"""
        # 爆款小说特征库（基于经典成功案例）
        self.bestseller_patterns = {
            "悬疑推理": {
                "开篇特点": ["悬念设置", "事件冲击", "环境渲染"],
                "节奏控制": ["快慢结合", "悬念递进", "高潮迭起"],
                "人物塑造": ["多层次性格", "动机复杂", "关系网络"],
                "语言风格": ["简练有力", "氛围营造", "细节精准"],
                "情感元素": ["紧张感", "好奇心", "正义感"],
                "成功案例": ["东野圭吾式逻辑", "阿加莎式布局", "本格推理严谨性"]
            },
            "言情现代": {
                "开篇特点": ["人物吸引", "情境设置", "冲突预埋"],
                "节奏控制": ["情感波动", "甜虐结合", "张力维持"],
                "人物塑造": ["性格反差", "成长弧线", "化学反应"],
                "语言风格": ["情感细腻", "对话生动", "内心描写"],
                "情感元素": ["心动感", "共情点", "治愈性"],
                "成功案例": ["现实感强", "情感真实", "代入感佳"]
            },
            "玄幻奇幻": {
                "开篇特点": ["世界观展示", "力量体系", "主角特色"],
                "节奏控制": ["升级节奏", "冒险探索", "战斗激烈"],
                "人物塑造": ["成长型主角", "师友敌配", "背景丰富"],
                "语言风格": ["气势磅礴", "想象丰富", "战斗精彩"],
                "情感元素": ["热血感", "成就感", "归属感"],
                "成功案例": ["体系完整", "逻辑自洽", "爽点密集"]
            }
        }
        
        # 质量评判标准
        self.quality_standards = {
            "逻辑连贯性": {
                "优秀": "前后呼应完美，无逻辑漏洞，伏笔自然",
                "良好": "基本连贯，偶有小疏漏，整体合理", 
                "及格": "主线清晰，支线略乱，需要优化",
                "不及格": "前后矛盾，逻辑混乱，需要重写"
            },
            "情感共鸣": {
                "优秀": "情感真实细腻，读者强烈共鸣，有温度感",
                "良好": "情感表达到位，有一定感染力",
                "及格": "情感描写平实，缺乏深度",
                "不及格": "情感虚假做作，无法引起共鸣"
            },
            "人物塑造": {
                "优秀": "人物立体丰满，性格鲜明，行为逻辑合理",
                "良好": "人物特点明确，有一定深度",
                "及格": "人物基本合格，略显平面",
                "不及格": "人物扁平化，标签式存在"
            }
        }
    
    def analyze_bestseller_patterns(self, genre: str, sample_texts: List[str]) -> Dict[str, Any]:
        """分析爆款小说模式"""
        logger.info(f"开始分析{genre}类型爆款小说模式")
        
        if not sample_texts:
            return {"error": "需要提供样本文本"}
        
        # 使用LLM分析爆款特征
        analysis_prompt = f"""
作为资深文学分析师，请深度分析以下{genre}类型的爆款小说样本，总结成功模式：

样本文本：
{chr(10).join(sample_texts[:3])}  # 只分析前3个样本

请从以下8个维度进行分析：
1. 逻辑结构特点（如何保持连贯性）
2. 情感表达方式（如何引起共鸣）
3. 原创元素运用（创新点在哪里）
4. 人物塑造手法（如何立体化）
5. 语言风格特色（避免AI痕迹的方法）
6. 节奏控制技巧（张弛有度的秘诀）
7. 主题深度体现（思想内涵表达）
8. 文化元素融入（真实感营造）

请用JSON格式输出分析结果：
{{
    "genre": "{genre}",
    "success_patterns": {{
        "logic_coherence": ["特点1", "特点2", "特点3"],
        "emotional_resonance": ["方法1", "方法2", "方法3"],
        "originality": ["创新点1", "创新点2", "创新点3"],
        "character_depth": ["技巧1", "技巧2", "技巧3"],
        "language_style": ["特色1", "特色2", "特色3"],
        "narrative_rhythm": ["节奏1", "节奏2", "节奏3"],
        "theme_depth": ["深度1", "深度2", "深度3"],
        "cultural_authenticity": ["元素1", "元素2", "元素3"]
    }},
    "key_techniques": ["核心技巧1", "核心技巧2", "核心技巧3"],
    "common_patterns": ["模式1", "模式2", "模式3"]
}}
"""
        
        try:
            analysis_result = self.llm.generate(analysis_prompt, max_tokens=3000, temperature=0.3)
            
            # 解析分析结果
            try:
                pattern_data = json.loads(analysis_result)
                
                # 更新模式库
                if genre not in self.bestseller_patterns:
                    self.bestseller_patterns[genre] = {}
                
                self.bestseller_patterns[genre].update(pattern_data.get("success_patterns", {}))
                
                # 保存学习结果
                self._save_learning_data(genre, pattern_data)
                
                return {
                    "success": True,
                    "patterns": pattern_data,
                    "message": f"成功分析{genre}类型爆款模式"
                }
                
            except json.JSONDecodeError:
                logger.warning("LLM返回结果不是有效JSON，尝试文本解析")
                return {
                    "success": False,
                    "raw_analysis": analysis_result,
                    "message": "分析完成但格式需要调整"
                }
                
        except Exception as e:
            logger.error(f"爆款模式分析失败: {e}")
            return {"success": False, "error": str(e)}
    
    def solve_core_problems(self, content: str, context: Dict[str, Any], 
                          target_problems: List[int] = None) -> Dict[str, Any]:
        """解决8大核心问题"""
        if target_problems is None:
            target_problems = list(range(1, 9))  # 默认解决所有问题
        
        logger.info(f"开始解决核心问题: {target_problems}")
        
        improved_content = content
        applied_solutions = []
        problem_scores = {}
        
        for problem_id in target_problems:
            if problem_id in self.problem_solvers:
                try:
                    solver_result = self.problem_solvers[problem_id](improved_content, context)
                    
                    if solver_result.get('improved', False):
                        improved_content = solver_result['content']
                        applied_solutions.append(solver_result['solution_name'])
                        problem_scores[problem_id] = solver_result.get('score', 0)
                    
                except Exception as e:
                    logger.error(f"解决问题{problem_id}失败: {e}")
                    problem_scores[problem_id] = 0
        
        return {
            'success': len(applied_solutions) > 0,
            'improved_content': improved_content,
            'applied_solutions': applied_solutions,
            'problem_scores': problem_scores,
            'overall_improvement': sum(problem_scores.values()) / len(problem_scores) if problem_scores else 0
        }
    
    def _solve_logic_coherence(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """解决逻辑连贯性问题"""
        genre = context.get('genre', '通用')
        patterns = self.bestseller_patterns.get(genre, {})
        
        prompt = f"""
作为逻辑专家，请解决以下文本的逻辑连贯性问题：

原文：
{content}

参考模式：{patterns.get('logic_coherence', [])}

逻辑连贯性优化要求：
1. 检查并修复前后矛盾（如角色设定前后不一）
2. 确保时间线合理（事件发生顺序逻辑）
3. 保证因果关系清晰（行为动机合理）
4. 强化细节呼应（前面的伏笔后面要有回应）
5. 维护世界观一致（设定规则不能自相矛盾）
6. 角色行为符合性格（避免OOC问题）

特别注意解决以下常见逻辑问题：
- 角色设定前后矛盾（如父母双亡后又出现打电话给爸爸）
- 时间线混乱（事件发生顺序不合理）
- 伏笔遗漏（前面提到的重要信息后面没有处理）
- 角色动机不明（行为缺乏合理解释）

如果发现逻辑问题，请修复并输出完整优化后的内容。
如果逻辑已经很好，请回复"LOGIC_COHERENT"。
"""
        
        try:
            result = self.llm.generate(prompt, max_tokens=4000, temperature=0.4)
            
            if result.strip() == "LOGIC_COHERENT":
                return {'improved': False, 'content': content, 'solution_name': '逻辑连贯性', 'score': 9.0}
            else:
                return {'improved': True, 'content': result, 'solution_name': '逻辑连贯性优化', 'score': 8.5}
                
        except Exception as e:
            logger.error(f"逻辑连贯性优化失败: {e}")
            return {'improved': False, 'content': content, 'solution_name': '逻辑连贯性', 'score': 0}
    
    def _solve_emotional_resonance(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """解决情感共鸣问题"""
        genre = context.get('genre', '通用')
        patterns = self.bestseller_patterns.get(genre, {})
        
        prompt = f"""
作为情感表达专家，请增强以下文本的情感共鸣：

原文：
{content}

参考模式：{patterns.get('emotional_resonance', [])}

情感共鸣增强要求：
1. 情感表达真实细腻（避免空洞抒情）
2. 用具体细节传达情感（而非抽象词汇堆砌）
3. 挖掘人性共通点（普世情感体验）
4. 营造代入感（让读者身临其境）
5. 情感层次丰富（不只是表面情绪）
6. 通过行为和对话显示情感（而非直接说教）

特别优化以下情感表达问题：
- 情感描写做作虚假（如过度煽情）
- 缺乏生活质感（脱离真实体验）
- 情感单调乏味（只有表面情绪）
- 无法引起共鸣（读者无感）

请输出情感共鸣增强后的内容：
"""
        
        try:
            result = self.llm.generate(prompt, max_tokens=4000, temperature=0.6)
            return {'improved': True, 'content': result, 'solution_name': '情感共鸣增强', 'score': 8.0}
            
        except Exception as e:
            logger.error(f"情感共鸣优化失败: {e}")
            return {'improved': False, 'content': content, 'solution_name': '情感共鸣', 'score': 0}
    
    def _solve_originality(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """解决原创性问题"""
        genre = context.get('genre', '通用')
        patterns = self.bestseller_patterns.get(genre, {})
        
        prompt = f"""
作为创意专家，请增强以下文本的原创性：

原文：
{content}

参考模式：{patterns.get('originality', [])}

原创性增强要求：
1. 避免常见套路（如霸道总裁、废材逆袭等老梗）
2. 创新情节设置（独特的冲突和转折）
3. 新颖人物设定（避免刻板印象）
4. 独特视角表达（不落俗套的叙述方式）
5. 创意元素融入（新鲜有趣的设定）
6. 颠覆常规期待（出人意料但合理）

特别避免以下原创性问题：
- 情节老套乏味（千篇一律的桥段）
- 人物设定陈旧（标签化角色）
- 缺乏新意（重复已有模式）
- 预测性过强（读者一眼看穿）

请输出原创性增强后的内容：
"""
        
        try:
            result = self.llm.generate(prompt, max_tokens=4000, temperature=0.8)
            return {'improved': True, 'content': result, 'solution_name': '原创性增强', 'score': 7.5}
            
        except Exception as e:
            logger.error(f"原创性优化失败: {e}")
            return {'improved': False, 'content': content, 'solution_name': '原创性', 'score': 0}
    
    def _solve_character_depth(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """解决人物塑造扁平化问题"""
        genre = context.get('genre', '通用')
        patterns = self.bestseller_patterns.get(genre, {})
        
        prompt = f"""
作为人物塑造专家，请让以下文本中的人物更加立体：

原文：
{content}

参考模式：{patterns.get('character_depth', [])}

人物立体化要求：
1. 多维度性格（非黑即白→复杂人性）
2. 独特行为习惯（个人特色和小癖好）
3. 清晰动机驱动（行为背后的深层原因）
4. 成长变化轨迹（人物弧线发展）
5. 真实对话风格（符合身份和性格）
6. 内心冲突矛盾（人性的复杂面）

特别解决以下人物问题：
- 标签化角色（如反派只会"冷笑眯眼"）
- 行为缺乏逻辑（角色行为不符合设定）
- 对话千人一面（没有个人特色）
- 缺乏成长性（从头到尾没变化）

请输出人物立体化后的内容：
"""
        
        try:
            result = self.llm.generate(prompt, max_tokens=4000, temperature=0.7)
            return {'improved': True, 'content': result, 'solution_name': '人物立体化', 'score': 8.2}
            
        except Exception as e:
            logger.error(f"人物塑造优化失败: {e}")
            return {'improved': False, 'content': content, 'solution_name': '人物塑造', 'score': 0}
    
    def _solve_ai_language(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """解决AI语言僵化问题"""
        genre = context.get('genre', '通用')
        patterns = self.bestseller_patterns.get(genre, {})
        
        prompt = f"""
作为语言大师，请消除以下文本的AI痕迹，让语言更自然：

原文：
{content}

参考模式：{patterns.get('language_style', [])}

语言自然化要求：
1. 消除程式化表达（如"深深地感受到"）
2. 避免无意义华丽辞藻（如"数第37根雨丝"）
3. 对话口语化生动（符合角色身份）
4. 句式灵活多变（长短结合，有节奏）
5. 用词精准有力（避免空洞堆砌）
6. 情景化表达（具体而非抽象）

特别消除以下AI语言问题：
- 副词过度使用（深深地、静静地、慢慢地）
- 套路化描写（在阳光下、眼中闪过一丝）
- 对话生硬正式（缺乏个性和口语感）
- 句式单调重复（结构过于程式化）

请输出语言自然化后的内容：
"""
        
        try:
            result = self.llm.generate(prompt, max_tokens=4000, temperature=0.6)
            return {'improved': True, 'content': result, 'solution_name': 'AI语言优化', 'score': 8.8}
            
        except Exception as e:
            logger.error(f"AI语言优化失败: {e}")
            return {'improved': False, 'content': content, 'solution_name': 'AI语言', 'score': 0}
    
    def _solve_narrative_rhythm(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """解决叙事节奏问题"""
        genre = context.get('genre', '通用')
        patterns = self.bestseller_patterns.get(genre, {})
        
        prompt = f"""
作为节奏控制专家，请优化以下文本的叙事节奏：

原文：
{content}

参考模式：{patterns.get('narrative_rhythm', [])}

叙事节奏优化要求：
1. 关键情节详写（重要场面详细描述）
2. 过渡情节简写（避免冗余描述）
3. 紧张场面加速（短句快节奏）
4. 抒情场面放缓（舒展有韵律）
5. 张弛有度控制（避免平铺直叙）
6. 悬念点恰当（保持读者兴趣）

特别解决以下节奏问题：
- 重要情节描述不够（该详写的地方太简略）
- 无关细节过多（在关键时刻还描述无关事物）
- 节奏单调平淡（缺乏起伏变化）
- 拖沓冗长（不会"做减法"）

请输出节奏优化后的内容：
"""
        
        try:
            result = self.llm.generate(prompt, max_tokens=4000, temperature=0.5)
            return {'improved': True, 'content': result, 'solution_name': '叙事节奏优化', 'score': 7.8}
            
        except Exception as e:
            logger.error(f"叙事节奏优化失败: {e}")
            return {'improved': False, 'content': content, 'solution_name': '叙事节奏', 'score': 0}
    
    def _solve_theme_depth(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """解决主题思想浅薄问题"""
        genre = context.get('genre', '通用')
        patterns = self.bestseller_patterns.get(genre, {})
        
        prompt = f"""
作为文学深度专家，请增强以下文本的主题深度：

原文：
{content}

参考模式：{patterns.get('theme_depth', [])}

主题深度增强要求：
1. 融入人性思考（对人性的深层探讨）
2. 社会现实反映（与现实生活的联系）
3. 价值观传达（积极正向的人生观）
4. 隐喻象征运用（文学手法的巧妙使用）
5. 哲理思辨融入（引发读者思考）
6. 情理并茂表达（既有情感又有理性）

特别提升以下主题问题：
- 内容浅薄无深度（只有表面情节）
- 缺乏思想内核（没有精神追求）
- 价值观模糊（缺乏正确导向）
- 文学性不足（纯粹娱乐化）

请输出主题深度增强后的内容：
"""
        
        try:
            result = self.llm.generate(prompt, max_tokens=4000, temperature=0.4)
            return {'improved': True, 'content': result, 'solution_name': '主题深度增强', 'score': 7.3}
            
        except Exception as e:
            logger.error(f"主题深度优化失败: {e}")
            return {'improved': False, 'content': content, 'solution_name': '主题深度', 'score': 0}
    
    def _solve_cultural_authenticity(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """解决文化适配性问题"""
        genre = context.get('genre', '通用')
        patterns = self.bestseller_patterns.get(genre, {})
        setting = context.get('setting', '现代都市')
        
        prompt = f"""
作为文化专家，请增强以下文本的文化真实感：

原文：
{content}

背景设定：{setting}
参考模式：{patterns.get('cultural_authenticity', [])}

文化真实性增强要求：
1. 地域特色融入（方言、习俗、建筑等）
2. 时代背景准确（历史文化细节）
3. 社会环境真实（生活场景描写）
4. 人文情怀体现（民族文化传承）
5. 生活细节具体（真实可感的日常）
6. 文化内涵深层（不只是表面符号）

特别优化以下文化问题：
- 文化元素平均化（失去地域特色）
- 时代感错位（现代和古代混杂）
- 生活细节虚假（脱离实际情况）
- 文化理解浅薄（只有表面认知）

请输出文化真实性增强后的内容：
"""
        
        try:
            result = self.llm.generate(prompt, max_tokens=4000, temperature=0.6)
            return {'improved': True, 'content': result, 'solution_name': '文化真实性增强', 'score': 7.6}
            
        except Exception as e:
            logger.error(f"文化适配性优化失败: {e}")
            return {'improved': False, 'content': content, 'solution_name': '文化适配性', 'score': 0}
    
    def learn_from_bestsellers(self, genre: str, reference_novels: List[str]) -> Dict[str, Any]:
        """从爆款小说中学习"""
        logger.info(f"开始学习{genre}类型的爆款小说")
        
        if not reference_novels:
            return {"success": False, "error": "需要提供参考小说"}
        
        # 模拟分析爆款小说特征（实际使用时可以接入真实的小说数据）
        learning_prompt = f"""
作为文学分析师，请分析{genre}类型的以下爆款小说，提取成功要素：

参考小说：
{chr(10).join(reference_novels)}

请分析以下成功要素：
1. 开篇吸引力技巧
2. 人物塑造方法
3. 情节推进节奏
4. 语言风格特色
5. 情感共鸣点设置
6. 悬念营造手法
7. 高潮设计技巧
8. 结局处理方式

请提供具体的学习要点和可应用的写作技巧。
"""
        
        try:
            learning_result = self.llm.generate(learning_prompt, max_tokens=3000, temperature=0.3)
            
            # 更新学习数据库
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            learning_data = {
                "genre": genre,
                "learning_time": timestamp,
                "analysis_result": learning_result,
                "reference_count": len(reference_novels)
            }
            
            self._save_learning_data(f"{genre}_learning", learning_data)
            
            return {
                "success": True,
                "learning_data": learning_data,
                "message": f"成功学习{len(reference_novels)}部{genre}爆款小说"
            }
            
        except Exception as e:
            logger.error(f"爆款小说学习失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _save_learning_data(self, data_type: str, data: Dict[str, Any]):
        """保存学习数据"""
        try:
            data_dir = "data/learning"
            os.makedirs(data_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{data_dir}/{data_type}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"学习数据已保存: {filename}")
            
        except Exception as e:
            logger.error(f"保存学习数据失败: {e}")
    
    def get_quality_report(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """获取内容质量报告"""
        try:
            # 分析8大核心问题
            problem_analysis = {}
            
            for problem_id in range(1, 9):
                problem_names = [
                    "逻辑连贯性", "情感共鸣", "原创性", "人物塑造",
                    "AI语言问题", "叙事节奏", "主题深度", "文化适配性"
                ]
                
                if problem_id <= len(problem_names):
                    problem_name = problem_names[problem_id - 1]
                    # 简化版质量评估
                    score = self._evaluate_problem_score(content, problem_id, context)
                    problem_analysis[problem_name] = {
                        'score': score,
                        'level': self._get_quality_level(score),
                        'suggestions': self._get_improvement_suggestions(problem_id, score)
                    }
            
            # 计算总体评分
            total_score = sum(p['score'] for p in problem_analysis.values()) / len(problem_analysis)
            
            return {
                'success': True,
                'overall_score': total_score,
                'overall_level': self._get_quality_level(total_score),
                'problem_analysis': problem_analysis,
                'priority_improvements': self._get_priority_improvements(problem_analysis)
            }
            
        except Exception as e:
            logger.error(f"质量报告生成失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def _evaluate_problem_score(self, content: str, problem_id: int, context: Dict[str, Any]) -> float:
        """评估特定问题的分数"""
        # 简化版评估逻辑
        base_score = 6.0
        
        if problem_id == 1:  # 逻辑连贯性
            # 检查是否有明显逻辑错误
            if "父母双亡" in content and ("爸爸" in content or "妈妈" in content):
                base_score = 3.0
            elif len(re.findall(r'[。！？]', content)) < 10:
                base_score = 5.0
            else:
                base_score = 7.5
                
        elif problem_id == 2:  # 情感共鸣
            emotion_words = ['感动', '心痛', '温暖', '幸福', '难过', '愤怒']
            emotion_count = sum(content.count(word) for word in emotion_words)
            base_score = min(8.0, 5.0 + emotion_count * 0.5)
            
        elif problem_id == 5:  # AI语言问题
            ai_patterns = ['深深地', '静静地', '慢慢地', '然而却']
            ai_count = sum(content.count(pattern) for pattern in ai_patterns)
            base_score = max(3.0, 9.0 - ai_count * 0.5)
            
        return base_score
    
    def _get_quality_level(self, score: float) -> str:
        """获取质量等级"""
        if score >= 8.5:
            return "优秀"
        elif score >= 7.0:
            return "良好"
        elif score >= 6.0:
            return "及格"
        else:
            return "不及格"
    
    def _get_improvement_suggestions(self, problem_id: int, score: float) -> List[str]:
        """获取改进建议"""
        suggestions_map = {
            1: ["检查角色设定一致性", "确保时间线合理", "强化因果关系"],
            2: ["增加情感细节描写", "使用具体生活场景", "挖掘人性共通点"],
            3: ["避免常见套路", "创新情节设置", "增加独特元素"],
            4: ["丰富人物性格", "添加行为习惯", "设置成长弧线"],
            5: ["消除程式化表达", "优化对话风格", "增加语言变化"],
            6: ["调整叙事节奏", "突出重点情节", "减少冗余描述"],
            7: ["融入人性思考", "增加文学深度", "强化主题表达"],
            8: ["增加文化元素", "细化地域特色", "提升真实感"]
        }
        
        base_suggestions = suggestions_map.get(problem_id, ["需要优化"])
        
        if score < 6.0:
            return base_suggestions + ["建议重点优化"]
        elif score < 7.0:
            return base_suggestions[:2]
        else:
            return base_suggestions[:1]
    
    def _get_priority_improvements(self, problem_analysis: Dict[str, Any]) -> List[str]:
        """获取优先改进项目"""
        sorted_problems = sorted(
            problem_analysis.items(),
            key=lambda x: x[1]['score']
        )
        
        return [problem for problem, analysis in sorted_problems[:3] if analysis['score'] < 7.0]
