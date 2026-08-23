"""内容生成Agent - 负责生成章节正文（已集成人性化与质量优化管线）"""
import re
from collections import Counter

import json
from utils import LLMClient, Storage, config
from utils.lorebook import Lorebook
from .prompts import (
    CONTENT_GENERATION_AGENT_SYSTEM_PROMPT,
    CONTENT_GENERATION_AGENT_PROMPT_TEMPLATE,
    CONTENT_OPTIMIZATION_PROMPT_TEMPLATE
)
# 可选的人性化与质量优化组件
try:
    from utils.text_humanizer import TextHumanizer
    from utils.quality_analyzer import QualityAnalyzer
    from utils.style_optimizer import StyleOptimizer
except Exception:
    TextHumanizer = None
    QualityAnalyzer = None
    StyleOptimizer = None

class ContentGenerationAgent:
    """内容生成Agent"""

    def __init__(self):
        self.llm = LLMClient()
        self.storage = Storage()
        # 世界观词典（轻量Lorebook）
        try:
            self.lorebook = Lorebook()
        except Exception:
            self.lorebook = None
        # 初始化可选优化组件
        self.humanizer = TextHumanizer(self.llm) if TextHumanizer else None
        self.analyzer = QualityAnalyzer() if QualityAnalyzer else None
        self.styler = StyleOptimizer(self.llm) if StyleOptimizer else None

    def generate_chapter(self, chapter_number, chapter_plan, outline=None):
        """
        生成章节内容（可选启用人性化与质量优化）
        """
        print("=" * 50)
        print(f"内容生成Agent开始生成第{chapter_number}章...")
        print("=" * 50)

        # 加载大纲
        if outline is None:
            outline = self.storage.load_outline()
        if not outline:
            print("✗ 未找到小说大纲")
            return None

        # 准备生成所需的信息
        target_word_count = chapter_plan.get('word_count', config.get('chapter.default_length', 3000))
        character_info = self._format_character_info(outline.get('main_characters', []))
        world_setting = outline.get('world_setting', '')
        style_guide = outline.get('style_guide', {})

        # 构建提示词
        system_prompt = CONTENT_GENERATION_AGENT_SYSTEM_PROMPT.format(
            narrative_perspective=style_guide.get('narrative_perspective', '第三人称全知视角'),
            language_style=style_guide.get('language_style', '现代白话，简洁流畅'),
            description_density=style_guide.get('description_density', '适中，重点场景详细描写')
        )
        # 轻量DOC提示与Lorebook注入
        doc_hint = ""
        if bool(config.get('generation.doc_light', True)):
            pmin = int(config.get('generation.paragraphs_min', 6))
            pmax = int(config.get('generation.paragraphs_max', 8))
            doc_hint = f"\n\n【写作要求-分段结构】本章请分为{pmin}~{pmax}个自然段，合理安排承接/推进/转折/收束；段间注意自然过渡（时间/空间/因果/情绪）。"
        lore_context = self._append_lorebook_context(
            base_text=f"{world_setting}\n{chapter_plan}",
            max_entries=3
        )
        user_prompt = CONTENT_GENERATION_AGENT_PROMPT_TEMPLATE.format(
            chapter_number=chapter_number,
            chapter_plan=json.dumps(chapter_plan, ensure_ascii=False, indent=2),
            target_word_count=target_word_count,
            character_info=character_info,
            world_setting=(world_setting or "") + ("\n" + lore_context if lore_context else ""),
            style_guide=json.dumps(style_guide, ensure_ascii=False, indent=2)
        ) + doc_hint

        # 调用LLM生成内容（带采样预设）
        sampling = self._choose_sampling_preset(chapter_plan)
        print(f"\n正在生成第{chapter_number}章内容（目标{target_word_count}字）...")
        print("这可能需要一些时间...\n")
        content = self.llm.generate_with_system_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=sampling.get('temperature', 0.8),
            max_tokens=int(target_word_count * 2),
            top_p=sampling.get('top_p'),
            presence_penalty=sampling.get('presence_penalty'),
            frequency_penalty=sampling.get('frequency_penalty')
        )

        # 提取标题和正文
        title, body = self._extract_title_and_body(content, chapter_plan.get('chapter_title', f'第{chapter_number}章'))
        original_body = body
        quality_before = None
        quality_after = None

        # 可选的人性化与质量优化
        if config.get('humanize.enabled', True) and self.humanizer and self.analyzer and self.styler:
            mode = str(config.get('humanize.mode', 'high')).lower()
            max_iters = config.get('humanize.max_iterations', 2)
            mode_iters_map = {'standard': 1, 'high': 2, 'premium': 3}
            iters = min(max_iters, mode_iters_map.get(mode, 2))

            # 初始质量分析
            quality_before = self.analyzer.analyze(body)
            current_text = body

            for i in range(iters):
                # 文本人性化
                humanized = self.humanizer.humanize(current_text, aggressive=(i > 0))
                current_text = humanized.get('humanized_text', current_text)

                # 风格优化（根据章节类型微调）
                style_prefs = {
                    'vivid_description': chapter_plan.get('chapter_type') in ('opening', 'development'),
                    'dialogue_variation': True,
                    'rhythm_adjustment': chapter_plan.get('pacing', 'normal') in ('fast', 'climax'),
                    'expression_personalization': True
                }
                styled = self.styler.optimize(current_text, style_prefs)
                current_text = styled.get('optimized_text', current_text)

                # 质量复评
                qa = self.analyzer.analyze(current_text)
                # 若达到目标或已显著提升，则可提前停止
                targets = {
                    'overall': float(config.get('humanize.targets.overall_score', 85.0)),
                    'human': float(config.get('humanize.targets.human_score', 80.0)),
                    'ai': float(config.get('humanize.targets.ai_score', 20.0)),
                }
                if qa['overall_score'] >= targets['overall'] and \
                   qa['ai_patterns']['human_score'] >= targets['human'] and \
                   qa['ai_patterns']['ai_score'] <= targets['ai']:
                    quality_after = qa
                    break
                quality_after = qa

            # 若优化后评分更好，则采用优化结果
            if quality_after and quality_before and quality_after['overall_score'] > quality_before['overall_score']:
                body = current_text

        # 构建章节数据
        chapter_data = {
            'chapter_number': chapter_number,
            'title': title,
            'content': body,
            'plan': chapter_plan,
            'word_count': len(body)
        }
        if quality_before:
            chapter_data['quality_before'] = {
                'overall_score': quality_before.get('overall_score'),
                'ai_score': quality_before.get('ai_patterns', {}).get('ai_score'),
                'human_score': quality_before.get('ai_patterns', {}).get('human_score')
            }
        if quality_after:
            chapter_data['quality_after'] = {
                'overall_score': quality_after.get('overall_score'),
                'ai_score': quality_after.get('ai_patterns', {}).get('ai_score'),
                'human_score': quality_after.get('ai_patterns', {}).get('human_score')
            }

        # 保存章节
        self.storage.save_chapter(chapter_number, chapter_data)

        print(f"\n✓ 第{chapter_number}章生成完成")
        print(f"标题: {title}")
        print(f"字数: {len(body)} (原始: {len(original_body)})")
        if quality_after:
            print(f"质量: {quality_after['overall_score']:.1f} / 人类感: {quality_after['ai_patterns']['human_score']:.1f} / AI感: {quality_after['ai_patterns']['ai_score']:.1f}")
        print("=" * 50)

        return chapter_data

    def optimize_chapter(self, chapter_number, feedback):
        """优化章节内容"""
        print("=" * 50)
        print(f"内容生成Agent开始优化第{chapter_number}章...")
        print("=" * 50)
        original_chapter = self.storage.load_chapter(chapter_number)
        if not original_chapter:
            print(f"✗ 未找到第{chapter_number}章")
            return None
        original_content = f"第{chapter_number}章 {original_chapter['title']}\n\n{original_chapter['content']}"
        user_prompt = CONTENT_OPTIMIZATION_PROMPT_TEMPLATE.format(
            chapter_number=chapter_number,
            original_content=original_content,
            feedback=feedback
        )
        print(f"\n正在优化第{chapter_number}章...")
        optimized_content = self.llm.chat(
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7,
            max_tokens=4000
        )
        title, body = self._extract_title_and_body(optimized_content, original_chapter['title'])
        updates = {
            'title': title,
            'content': body,
            'word_count': len(body),
            'optimization_feedback': feedback
        }
        self.storage.update_chapter(chapter_number, updates)
        print(f"\n✓ 第{chapter_number}章优化完成")
        print(f"新字数: {len(body)}")
        print("=" * 50)
        return updates

    def _format_character_info(self, characters):
        """格式化人物信息"""
        if not characters:
            return "暂无人物信息"
        info_lines = []
        for char in characters:
            if isinstance(char, dict):
                name = char.get('name', '未知')
                role = char.get('role', '')
                personality = char.get('personality', '')
                background = char.get('background', '')
                info_lines.append(f"- {name}（{role}）：{personality}。{background}")
        return "\n".join(info_lines) if info_lines else "暂无人物信息"

    def _extract_title_and_body(self, content, default_title):
        """从生成的内容中提取标题和正文"""
        lines = content.strip().split('\n')
        if lines and ('章' in lines[0] or 'Chapter' in lines[0]):
            title = lines[0].strip().replace('#', '').strip()
            body = '\n'.join(lines[1:]).strip()
        else:
            title = default_title
            body = content.strip()
        return title, body

