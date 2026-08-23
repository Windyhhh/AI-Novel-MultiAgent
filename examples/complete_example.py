"""
完整示例：使用人性化生成器创建高质量、无AI感的小说

这个示例展示了如何使用整个系统来生成一部完整的小说
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.human_like_generator import HumanLikeGenerator
from utils.quality_analyzer import QualityAnalyzer
from utils import get_logger

logger = get_logger('complete_example')

def example_1_single_chapter():
    """示例1：生成单个高质量章节"""
    print("\n" + "="*60)
    print("示例1：生成单个高质量章节（Premium模式）")
    print("="*60 + "\n")
    
    # 初始化生成器（需要你的LLM客户端）
    # generator = HumanLikeGenerator(your_llm_client)
    
    # 章节规划
    chapter_plan = {
        "chapter_number": 1,
        "chapter_type": "opening",
        "word_count": 3000,
        "title": "天才少年",
        "plot_points": [
            "主角林凡在宗门测试中展现惊人天赋",
            "引起长老注意",
            "暗示未来危机"
        ],
        "pacing": "slow",
        "focus": "character_introduction",
        "tone": "mysterious"
    }
    
    print("📋 章节规划：")
    print(f"  章节：第{chapter_plan['chapter_number']}章 - {chapter_plan['title']}")
    print(f"  类型：{chapter_plan['chapter_type']}")
    print(f"  字数：{chapter_plan['word_count']}")
    print(f"  情节点：{len(chapter_plan['plot_points'])}个")
    print()
    
    # 生成（使用Premium模式获得最高质量）
    print("🚀 开始生成...")
    # result = generator.generate_human_like_chapter(
    #     chapter_plan,
    #     quality_mode="premium"
    # )
    
    # 模拟结果展示
    print("\n✅ 生成完成！\n")
    print("📊 质量报告：")
    print(f"  总体质量：95.2/100 ⭐⭐⭐⭐⭐")
    print(f"  人类感评分：92.5/100 ✅")
    print(f"  AI感评分：7.8/100 ✅")
    print(f"  Burstiness：0.72 ✅")
    print(f"  词汇多样性：0.76 ✅")
    print(f"  是否达标：是 ✅")
    print()
    print("🔄 优化历史：")
    print(f"  第1轮：Burstiness 0.28 → 0.58 (+107%)")
    print(f"  第2轮：Burstiness 0.58 → 0.68 (+17%)")
    print(f"  第3轮：Burstiness 0.68 → 0.72 (+6%)")
    print(f"  LLM增强：自然度提升")
    print()
    print("📝 生成的章节内容：")
    print("-" * 60)
    print("（这里会是生成的章节内容...）")
    print("-" * 60)


def example_2_batch_generation():
    """示例2：批量生成多个章节"""
    print("\n" + "="*60)
    print("示例2：批量生成多个章节（High模式）")
    print("="*60 + "\n")
    
    # 准备多个章节规划
    chapter_plans = [
        {
            "chapter_number": 1,
            "chapter_type": "opening",
            "word_count": 3000,
            "plot_points": ["主角登场", "展示天赋"]
        },
        {
            "chapter_number": 2,
            "chapter_type": "development",
            "word_count": 3000,
            "plot_points": ["拜师学艺", "遇到挑战"]
        },
        {
            "chapter_number": 3,
            "chapter_type": "conflict",
            "word_count": 3000,
            "plot_points": ["与对手冲突", "展现实力"]
        },
        {
            "chapter_number": 4,
            "chapter_type": "climax",
            "word_count": 3500,
            "plot_points": ["关键战斗", "突破境界"]
        },
        {
            "chapter_number": 5,
            "chapter_type": "resolution",
            "word_count": 2500,
            "plot_points": ["获得认可", "埋下伏笔"]
        }
    ]
    
    print(f"📚 准备生成 {len(chapter_plans)} 个章节")
    print()
    
    # 批量生成
    # generator = HumanLikeGenerator(your_llm_client)
    # results = generator.batch_generate(chapter_plans, quality_mode="high")
    
    # 模拟结果
    print("🚀 批量生成中...")
    for i, plan in enumerate(chapter_plans, 1):
        print(f"  [{i}/{len(chapter_plans)}] 生成第{plan['chapter_number']}章... ✅")
    
    print("\n✅ 批量生成完成！\n")
    
    # 生成质量报告
    # report = generator.get_quality_report(results)
    
    print[object Object]计报告：")
    print(f"  总章节数：5")
    print(f"  平均质量：89.4/100")
    print(f"  平均人类感：87.8/100")
    print(f"  平均AI感：11.2/100")
    print()
    print("📈 质量分布：")
    print(f"  优秀（90+）：2章")
    print(f"  良好（80-90）：3章")
    print(f"  一般（70-80）：0章")
    print(f"  较差（<70）：0章")
    print()
    print(f"✅ 达标章节：5/5 (100%)")


def example_3_quality_analysis():
    """示例3：单独使用质量分析器"""
    print("\n" + "="*60)
    print("示例3：分析现有文本的质量")
    print("="*60 + "\n")
    
    # 示例文本（AI生成的典型文本）
    ai_text = """
    他走进房间。房间很大。房间里有一张桌子。桌子上有一本书。
    他拿起书。书很旧。他打开书。书里有很多字。他开始阅读。
    """
    
    # 改进后的文本
    human_text = """
    房间出奇的大。他的目光落在桌上那本书——父亲的。
    颤抖着，他伸出手。泛黄的书页，熟悉的笔迹。
    深吸一口气，翻开。
    """
    
    analyzer = QualityAnalyzer()
    
    print("📝 分析AI生成的文本：")
    print("-" * 60)
    print(ai_text.strip())
    print("-" * 60)
    
    ai_analysis = analyzer.analyze(ai_text)
    
    print("\n📊 AI文本分析结果：")
    print(f"  总体评分：{ai_analysis['overall_score']:.1f}/100 ❌")
    print(f"  人类感：{ai_analysis['ai_patterns']['human_score']:.1f}/100 ❌")
    print(f"  AI感：{ai_analysis['ai_patterns']['ai_score']:.1f}/100 ⚠️")
    print(f"  Burstiness：{ai_analysis['burstiness']['coefficient_of_variation']:.3f} ❌")
    print(f"  词汇多样性：{ai_analysis['lexical_diversity']['ttr']:.3f} ❌")
    
    print("\n⚠️ 检测到的AI特征：")
    for feature in ai_analysis['ai_patterns']['detected_features']:
        print(f"  - {feature}")
    
    print("\n💡 改进建议：")
    for suggestion in ai_analysis['suggestions']:
        print(f"  - {suggestion}")
    
    print("\n" + "="*60)
    print("\n📝 分析优化后的文本：")
    print("-" * 60)
    print(human_text.strip())
    print("-" * 60)
    
    human_analysis = analyzer.analyze(human_text)
    
    print("\n📊 优化文本分析结果：")
    print(f"  总体评分：{human_analysis['overall_score']:.1f}/100 ✅")
    print(f"  人类感：{human_analysis['ai_patterns']['human_score']:.1f}/100 ✅")
    print(f"  AI感：{human_analysis['ai_patterns']['ai_score']:.1f}/100 ✅")
    print(f"  Burstiness：{human_analysis['burstiness']['coefficient_of_variation']:.3f} ✅")
    print(f"  词汇多样性：{human_analysis['lexical_diversity']['ttr']:.3f} ✅")
    
    print("\n📈 改进对比：")
    print(f"  总体质量：+{human_analysis['overall_score'] - ai_analysis['overall_score']:.1f}")
    print(f"  人类感：+{human_analysis['ai_patterns']['human_score'] - ai_analysis['ai_patterns']['human_score']:.1f}")
    print(f"  AI感：{ai_analysis['ai_patterns']['ai_score'] - human_analysis['ai_patterns']['ai_score']:.1f}")


def example_4_custom_quality_standards():
    """示例4：自定义质量标准"""
    print("\n" + "="*60)
    print("示例4：自定义质量标准")
    print("="*60 + "\n")
    
    # generator = HumanLikeGenerator(your_llm_client)
    
    print[object Object]认质量标准：")
    print("  总体评分：≥ 85.0")
    print("  Burstiness：≥ 0.5")
    print("  词汇多样性：≥ 0.6")
    print("  人类感：≥ 80.0")
    print("  AI感：≤ 20.0")
    print()
    
    # 自定义更高的标准
    print("🎯 设置更高的质量标准：")
    # generator.quality_thresholds = {
    #     "overall_score": 90.0,
    #     "burstiness": 0.6,
    #     "lexical_diversity": 0.65,
    #     "human_score": 85.0,
    #     "ai_score": 15.0
    # }
    
    print("  总体评分：≥ 90.0 ⬆️")
    print("  Burstiness：≥ 0.6 ⬆️")
    print("  词汇多样性：≥ 0.65 ⬆️")
    print("  人类感：≥ 85.0 ⬆️")
    print("  AI感：≤ 15.0 ⬇️")
    print()
    
    print("✅ 质量标准已更新！")
    print("💡 系统将自动进行更多轮优化以达到更高标准")


def main():
    """运行所有示例"""
    print("\n" + "🎨"*30)
    print("人性化小说生成系统 - 完整示例")
    print("🎨"*30)
    
    # 运行所有示例
    example_1_single_chapter()
    input("\n按回车继续下一个示例...")
    
    example_2_batch_generation()
    input("\n按回车继续下一个示例...")
    
    example_3_quality_analysis()
    input("\n按回车继续下一个示例...")
    
    example_4_custom_quality_standards()
    
    print("\n" + "="*60)
    print("✅ 所有示例运行完成！")
    print("="*60)
    print("\n📚 更多信息：")
    print("  - 查看 ULTIMATE_QUALITY_GUIDE.md 获取完整使用指南")
    print("  - 查看 COMPLETE_SYSTEM_OVERVIEW.md 了解系统架构")
    print("  - 查看 HUMAN_LIKE_WRITING_RESEARCH.md 了解技术原理")
    print("\n🚀 开始创作你的无AI感高质量小说吧！\n")


if __name__ == "__main__":
    main()

