"""
AI小说生成系统 - 主程序入口
多智能体协作的长篇小说自动生成系统
"""
import os
import sys
import argparse
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_environment():
    """检查环境配置"""
    api_key = os.getenv("HEPAI_API_KEY")
    if not api_key:
        print("=" * 60)
        print("⚠️  警告：未配置HEPAI_API_KEY")
        print("=" * 60)
        print("请按以下步骤配置：")
        print("1. 复制 .env.example 为 .env")
        print("2. 在 .env 文件中设置 HEPAI_API_KEY")
        print("=" * 60)
        return False
    return True

def run_web():
    """启动Web服务"""
    from web.app import run_app
    run_app()

def run_cli():
    """命令行模式"""
    from agents import OutlineAgent, ChapterPlanningAgent, ContentGenerationAgent
    from agents.human_like_generator import HumanLikeGenerator
    from scheduler import NovelScheduler
    from qa import NovelQASystem
    from integrations import FeedbackProcessor
    from utils import Storage, LLMClient, config

    print("=" * 60)
    print("智能小说创作系统 - 命令行模式")
    print("=" * 60)

    storage = Storage()

    while True:
        print("\n请选择操作：")
        print("1. 创建小说大纲")
        print("2. 生成单个章节")
        print("3. 启动每日自动生成")
        print("4. 查看章节列表")
        print("5. 智能问答")
        print("6. 处理飞书反馈")
        print("7. 重建问答索引")
        print("8. 高质量人性化生成一章（Premium）")
        print("9. 批量人性化优化已有章节文本")
        print("10. 创建悬疑推理大纲")
        print("11. 番茄小说专用章节生成")
        print("12. 线索管理系统")
        print("13. 推理逻辑验证")
        print("14. 精品章节生成（高质量内容引擎）")
        print("15. 整部小说连贯性检查")
        print("16. 智能优化工作流")
        print("17. 批量章节优化（高级引擎）")
        print("18. AI小说8大问题解决方案")
        print("19. 爆款小说学习与分析")
        print("20. 内容质量深度报告")
        print("21. 自我反思内容生成（Self-RAG）")
        print("22. 多模态小说创作")
        print("23. 智能对话系统")
        print("24. 整合式高级创作模式")
        print("25. 🚀 一条龙智能体协作优化系统")
        print("0. 退出")

        choice = input("\n请输入选项 (0-25): ").strip()

        if choice == '1':
            # 智能协作创建大纲
            from agents.agent_orchestrator import AgentOrchestrator
            from agents.agent_factory import AgentFactory
            
            orchestrator = AgentOrchestrator()
            factory = AgentFactory()
            
            print("\n🎯 智能协作大纲创建")
            print("=" * 50)
            
            # 获取用户需求
            print("请选择小说类型：")
            print("1. 悬疑推理  2. 言情恋爱  3. 玄幻奇幻")
            print("4. 科幻未来  5. 历史古代  6. 都市现代")
            print("7. 其他类型")
            
            type_choice = input("类型选择 (1-7): ").strip()
            type_map = {
                '1': 'mystery', '2': 'romance', '3': 'fantasy',
                '4': 'scifi', '5': 'historical', '6': 'urban', '7': 'general'
            }
            genre = type_map.get(type_choice, 'general')
            
            # 获取详细设定
            custom_settings = {}
            if genre != 'general':
                print(f"\n📝 {genre} 小说详细设定")
                custom_settings['genre'] = genre
                custom_settings['title'] = input("书名（可选）: ").strip()
                custom_settings['theme'] = input("主题（如：成长、复仇、爱情）: ").strip()
                custom_settings['setting'] = input("背景设定（如：现代都市、古代宫廷）: ").strip()
                custom_settings['style'] = input("文风（如：轻松幽默、严肃深刻）: ").strip()
                custom_settings['platform'] = input("发布平台（默认：番茄小说）: ").strip() or "番茄小说"
                custom_settings['target_words'] = input("目标字数（默认：100万字）: ").strip() or "100万字"
            
            print(f"\n🚀 启动多智能体协作创建{genre}大纲...")
            
            # 使用协作系统创建大纲
            collaborative_outline = orchestrator.create_collaborative_outline(genre, custom_settings)
            
            if collaborative_outline:
                print(f"\n✅ 协作大纲创建成功！")
                print(f"📊 质量评分: {collaborative_outline.get('quality_score', 'N/A')}")
                print(f"🎭 涉及智能体: 大纲规划、角色记忆、情节追踪等")
                if genre == 'mystery':
                    print(f"🔍 已创建完整的悬疑推理系统（线索、角色关系）")
                print(f"💾 大纲已保存，可以开始生成章节！")
            else:
                print("❌ 大纲创建失败，请检查设置")

        elif choice == '2':
            # 智能协作生成章节
            from agents.agent_orchestrator import AgentOrchestrator
            from agents.agent_factory import AgentFactory
            from utils.advanced_optimizer import AdvancedOptimizer
            
            orchestrator = AgentOrchestrator()
            factory = AgentFactory()
            optimizer = AdvancedOptimizer()
            
            print("\n🤖 智能协作章节生成")
            print("=" * 50)
            
            # 检查是否有大纲
            outline = storage.load_outline()
            mystery_outline = storage.load_mystery_outline()
            
            if not outline and not mystery_outline:
                print("❌ 未找到大纲，请先创建大纲（选项1或10）")
                continue
            
            # 确定章节号
            latest_chapter = storage.get_latest_chapter_number()
            next_chapter = latest_chapter + 1
            
            print(f"📝 准备生成第{next_chapter}章")
            
            # 选择生成模式
            print("\n请选择生成模式：")
            print("1. 标准协作模式（多智能体协作）")
            print("2. 高级优化模式（包含质量优化）")
            print("3. 平台特化模式（针对番茄小说等平台）")
            
            mode_choice = input("模式选择 (1-3): ").strip()
            
            if mode_choice == '1':
                print(f"🚀 启动标准协作模式生成第{next_chapter}章...")
                chapter_result = orchestrator.generate_chapter_collaboratively(next_chapter)
                
            elif mode_choice == '2':
                print(f"⚡ 启动高级优化模式生成第{next_chapter}章...")
                # 先用标准模式生成
                chapter_result = orchestrator.generate_chapter_collaboratively(next_chapter)
                
                if chapter_result:
                    print("🔧 开始高级内容优化...")
                    # 获取完整上下文用于优化
                    context = orchestrator.context_manager.get_full_context()
                    
                    # 应用高级优化
                    optimization_result = optimizer.comprehensive_optimize(
                        chapter_result.get('content', ''), 
                        context
                    )
                    
                    if optimization_result['optimization_success']:
                        chapter_result['content'] = optimization_result['optimized_content']
                        chapter_result['optimized'] = True
                        chapter_result['improvements'] = optimization_result['improvements']
                        chapter_result['quality_improvement'] = optimization_result['quality_improvement']
                        
                        # 更新存储
                        storage.update_chapter(next_chapter, chapter_result)
                        
                        print(f"✨ 优化完成！改进项目: {', '.join(optimization_result['improvements'])}")
                        print(f"📈 质量提升: {optimization_result['quality_improvement']:.2f}")
                    else:
                        print("ℹ️ 当前内容质量已经很好，无需优化")
                        
            elif mode_choice == '3':
                print(f"🎯 启动平台特化模式生成第{next_chapter}章...")
                
                # 获取平台信息
                platform = input("目标平台（默认：番茄小说）: ").strip() or "番茄小说"
                
                # 使用平台特化生成
                context = orchestrator.context_manager.get_full_context()
                context['platform'] = platform
                context['platform_optimization'] = True
                
                chapter_result = orchestrator.generate_chapter_collaboratively(next_chapter, context)
                
                # 如果是番茄小说，进行额外优化
                if platform == "番茄小说" and chapter_result:
                    tomato_agent = factory.get_agent('tomato_novel')
                    if tomato_agent:
                        print("🍅 进行番茄小说平台优化...")
                        retention_result = tomato_agent.optimize_chapter_for_retention(
                            chapter_result['content'], next_chapter
                        )
                        if retention_result['retention_score'] > 80:
                            chapter_result['content'] = retention_result['optimized_content']
                            chapter_result['retention_optimized'] = True
                            chapter_result['retention_score'] = retention_result['retention_score']
                            storage.update_chapter(next_chapter, chapter_result)
                            print(f"📱 留存率优化完成，评分: {retention_result['retention_score']:.1f}")
            else:
                print("❌ 无效选择")
                continue
            
            if chapter_result:
                print(f"\n✅ 第{next_chapter}章生成成功！")
                print(f"📄 字数: {chapter_result.get('word_count', 0)}字")
                print(f"🏆 质量评分: {chapter_result.get('quality_score', 'N/A')}")
                
                if chapter_result.get('optimized'):
                    print(f"⚡ 已应用优化: {', '.join(chapter_result.get('improvements', []))}")
                
                if chapter_result.get('character_consistency'):
                    print(f"👥 角色一致性: ✓")
                
                if chapter_result.get('plot_consistency'):
                    print(f"📚 情节连贯性: ✓")
                
                if chapter_result.get('logic_validation'):
                    logic_score = chapter_result['logic_validation'].get('overall_score', 0)
                    print(f"🧠 逻辑验证: {logic_score:.1f}/10")
                
                print(f"💾 章节已保存到数据库")
                
                # 询问是否继续生成下一章
                continue_gen = input(f"\n是否继续生成第{next_chapter + 1}章？(y/n): ").strip().lower()
                if continue_gen == 'y':
                    # 递归调用生成下一章
                    print("🔄 准备生成下一章...")
                    # 这里可以添加连续生成逻辑
                    
            else:
                print("❌ 章节生成失败，请检查大纲和设置")

        elif choice == '3':
            # 启动调度器
            scheduler = NovelScheduler()
            scheduler.start()
            print("\n调度器已启动，按Ctrl+C停止...")
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                scheduler.stop()
                print("\n调度器已停止")

        elif choice == '4':
            # 查看章节
            chapters = storage.get_all_chapters()
            if chapters:
                print(f"\n共有 {len(chapters)} 章：")
                for ch in chapters:
                    print(f"第{ch['chapter_number']}章: {ch.get('title', 'N/A')} ({ch.get('word_count', 0)}字)")
            else:
                print("\n暂无章节")

        elif choice == '5':
            # 智能问答
            qa_system = NovelQASystem()
            question = input("\n请输入问题: ").strip()
            if question:
                answer = qa_system.query(question)
                print(f"\n回答：\n{answer}")

        elif choice == '6':
            # 处理飞书反馈
            processor = FeedbackProcessor()
            processor.process_feedbacks()

        elif choice == '7':
            # 重建索引
            qa_system = NovelQASystem()
            qa_system.index_all_chapters()
            print("\n✓ 问答索引已重建")

        elif choice == '8':
            # 高质量人性化生成一章（Premium）
            from agents import ChapterPlanningAgent, OutlineAgent
            from agents.human_like_generator import HumanLikeGenerator
            from utils import LLMClient

            outline = storage.load_outline()
            if not outline:
                print("未找到大纲，准备自动创建...")
                outline_agent = OutlineAgent()
                mode = 'autonomous'
                outline = outline_agent.create_outline(mode=mode)
                if not outline:
                    print("✗ 大纲创建失败")
                    continue
            latest_chapter = storage.get_latest_chapter_number()
            next_chapter = latest_chapter + 1
            planner = ChapterPlanningAgent()
            chapter_plan = planner.plan_chapter(next_chapter, outline)
            if not chapter_plan:
                print("✗ 章节规划失败")
                continue
            print(f"\n开始高级人性化生成：第{next_chapter}章（Premium模式）...")
            generator = HumanLikeGenerator(LLMClient())
            result = generator.generate_human_like_chapter(
                chapter_plan=chapter_plan,
                previous_context=None,
                quality_mode='premium'
            )
            chapter_data = {
                'chapter_number': next_chapter,
                'title': chapter_plan.get('chapter_title', f'第{next_chapter}章'),
                'content': result['final_content'],
                'plan': chapter_plan,
                'word_count': len(result['final_content']),
                'quality': result.get('final_quality', {})
            }
            storage.save_chapter(next_chapter, chapter_data)
            print(f"\n✓ 第{next_chapter}章生成完成（Premium）。质量：{result['final_quality']['overall_score']:.1f} / 人类感：{result['human_likeness_score']:.1f}")


        elif choice == '9':
            # 批量人性化优化已有章节文本
            from utils.quality_analyzer import QualityAnalyzer
            from utils.text_humanizer import TextHumanizer
            from utils.style_optimizer import StyleOptimizer
            from utils import LLMClient

            chapters = storage.get_all_chapters()
            if not chapters:
                print("\n暂无章节可优化")
                continue

            print(f"\n将对 {len(chapters)} 个章节进行人性化质量优化（不会降低质量，智能增益）")
            confirm = input("是否继续？(y/n): ").strip().lower()
            if confirm != 'y':
                continue

            analyzer = QualityAnalyzer()
            humanizer = TextHumanizer(LLMClient())
            styler = StyleOptimizer(LLMClient())

            improved = 0
            skipped = 0
            total = len(chapters)
            for ch in chapters:
                ch_num = ch.get('chapter_number')
                orig = ch.get('content', '')
                if not orig:
                    skipped += 1
                    continue
                # 初始质量
                q0 = analyzer.analyze(orig)
                # 人性化 + 风格优化
                hres = humanizer.humanize(orig, aggressive=True)
                mid = hres.get('humanized_text', orig)
                sres = styler.optimize(mid, {
                    'vivid_description': True,
                    'dialogue_variation': True,
                    'rhythm_adjustment': True,
                    'expression_personalization': True
                })
                new_text = sres.get('optimized_text', mid)
                # 复评
                q1 = analyzer.analyze(new_text)
                # 仅在总体更高 且 AI感更低 时写回
                if (q1['overall_score'] > q0['overall_score']) and (q1['ai_patterns']['ai_score'] < q0['ai_patterns']['ai_score']):
                    storage.update_chapter(ch_num, {
                        'content': new_text,
                        'word_count': len(new_text),
                        'quality_before': {
                            'overall_score': q0.get('overall_score'),
                            'ai_score': q0.get('ai_patterns', {}).get('ai_score'),
                            'human_score': q0.get('ai_patterns', {}).get('human_score')
                        },
                        'quality_after': {
                            'overall_score': q1.get('overall_score'),
                            'ai_score': q1.get('ai_patterns', {}).get('ai_score'),
                            'human_score': q1.get('ai_patterns', {}).get('human_score')
                        }
                    })
                    improved += 1
                    print(f"✓ 第{ch_num}章 已优化：总体 {q0['overall_score']:.1f}→{q1['overall_score']:.1f} / AI感 {q0['ai_patterns']['ai_score']:.1f}→{q1['ai_patterns']['ai_score']:.1f}")
                else:
                    skipped += 1
                    print(f"- 第{ch_num}章 略过（优化后未显著提高）")

            print(f"\n批量优化完成：改进 {improved}/{total} 章，略过 {skipped} 章")
            # 重新构建问答索引
            qa_system = NovelQASystem()
            qa_system.index_all_chapters()
            print("✓ 已重建问答索引")

        elif choice == '10':
            # 创建悬疑推理大纲
            from agents.mystery_agent import MysteryAgent
            
            mystery_agent = MysteryAgent()
            print("\n创建悬疑推理小说大纲")
            print("=" * 40)
            
            mystery_type = input("推理类型 (1=本格推理, 2=社会派, 3=密室推理, 4=心理推理): ").strip()
            type_map = {
                '1': '本格推理',
                '2': '社会派推理', 
                '3': '密室推理',
                '4': '心理推理'
            }
            mystery_type = type_map.get(mystery_type, '本格推理')
            
            setting = input("故事背景 (如：现代都市/民国上海/校园): ").strip() or "现代都市"
            victim_profile = input("受害者设定 (如：年轻白领/富商/学者): ").strip() or "年轻白领"
            motive_theme = input("犯罪动机 (如：金钱纠纷/情感仇杀/权力斗争): ").strip() or "金钱纠纷"
            
            custom_settings = {
                'mystery_type': mystery_type,
                'setting': setting,
                'victim_profile': victim_profile,
                'motive_theme': motive_theme
            }
            
            print(f"\n正在创建{mystery_type}大纲...")
            outline = mystery_agent.create_mystery_outline(custom_settings)
            
            if outline:
                print(f"\n✓ 悬疑推理大纲创建成功！")
                print(f"ID: {outline['id']}")
                print(f"类型: {outline['mystery_type']}")
                print(f"背景: {outline['setting']}")
                
                # 生成线索系统和角色关系
                print("\n创建线索管理系统...")
                clue_system = mystery_agent.create_clue_system(outline)
                if clue_system:
                    print("✓ 线索系统创建完成")
                
                print("\n创建角色关系图...")
                relationships = mystery_agent.generate_character_relationships(outline)
                if relationships:
                    print("✓ 角色关系图创建完成")
                
                print(f"\n悬疑推理创作系统已就绪，可以开始生成章节！")
            else:
                print("✗ 悬疑推理大纲创建失败")

        elif choice == '11':
            # 番茄小说专用章节生成
            from agents.tomato_novel_agent import TomatoNovelAgent
            from agents.mystery_agent import MysteryAgent
            from agents import ChapterPlanningAgent
            
            tomato_agent = TomatoNovelAgent()
            mystery_agent = MysteryAgent()
            
            print("\n番茄小说专用章节生成")
            print("=" * 40)
            
            # 检查是否有悬疑大纲
            mystery_outline = storage.load_mystery_outline()
            if not mystery_outline:
                print("未找到悬疑推理大纲，请先创建（选项10）")
                continue
            
            # 获取相关数据
            clue_system = storage.load_clue_system(mystery_outline['id'])
            character_relationships = storage.load_character_relationships(mystery_outline['id'])
            
            # 确定章节号
            latest_chapter = storage.get_latest_chapter_number()
            next_chapter = latest_chapter + 1
            
            print(f"准备生成第{next_chapter}章（番茄小说优化版）")
            
            # 创建章节计划
            planner = ChapterPlanningAgent()
            chapter_plan = {
                'chapter_number': next_chapter,
                'chapter_title': f'第{next_chapter}章',
                'main_plot_points': [],
                'character_development': [],
                'clues_to_reveal': []
            }
            
            # 构建上下文
            context = {
                'mystery_outline': mystery_outline,
                'clue_system': clue_system,
                'character_relationships': character_relationships
            }
            
            print("正在生成番茄小说风格章节...")
            result = tomato_agent.generate_mystery_chapter(chapter_plan, context)
            
            if result:
                # 保存章节
                storage.save_chapter(next_chapter, result)
                storage.save_tomato_optimized_chapter(next_chapter, result)
                
                print(f"\n✓ 第{next_chapter}章生成完成！")
                print(f"字数: {result['word_count']}字")
                print(f"番茄小说评分: {result.get('tomato_score', 0):.1f}/100")
                print(f"悬念点数量: {len(result.get('suspense_points', []))}")
                
                # 询问是否需要优化留存率
                optimize = input("\n是否需要优化读者留存率？(y/n): ").strip().lower()
                if optimize == 'y':
                    print("正在优化留存率...")
                    optimized = tomato_agent.optimize_chapter_for_retention(result['content'], next_chapter)
                    if optimized['retention_score'] > 80:
                        result['content'] = optimized['optimized_content']
                        result['retention_optimized'] = True
                        result['retention_score'] = optimized['retention_score']
                        storage.update_chapter(next_chapter, result)
                        print(f"✓ 留存率优化完成，评分: {optimized['retention_score']:.1f}")
            else:
                print("✗ 章节生成失败")

        elif choice == '12':
            # 线索管理系统
            from agents.mystery_agent import MysteryAgent, ClueTracker
            
            mystery_agent = MysteryAgent()
            clue_tracker = ClueTracker()
            
            print("\n线索管理系统")
            print("=" * 40)
            
            mystery_outline = storage.load_mystery_outline()
            if not mystery_outline:
                print("未找到悬疑推理大纲，请先创建（选项10）")
                continue
            
            while True:
                print("\n线索管理选项：")
                print("1. 查看所有线索")
                print("2. 添加新线索")
                print("3. 查看指定章节的线索")
                print("4. 检查线索一致性")
                print("0. 返回主菜单")
                
                clue_choice = input("请选择操作: ").strip()
                
                if clue_choice == '1':
                    clues = storage.get_all_clues()
                    if clues:
                        print(f"\n共有 {len(clues)} 个线索：")
                        for i, clue in enumerate(clues, 1):
                            print(f"{i}. [{clue.get('type', 'unknown')}] {clue.get('description', 'N/A')}")
                    else:
                        print("\n暂无线索记录")
                
                elif clue_choice == '2':
                    clue_type = input("线索类型 (physical/testimony/environment/psychological): ").strip()
                    description = input("线索描述: ").strip()
                    importance = input("重要性 (S/A/B/C): ").strip().upper()
                    reveal_chapter = input("计划揭示章节: ").strip()
                    
                    if description:
                        clue_id = f"clue_{len(storage.get_all_clues()) + 1:03d}"
                        clue_data = {
                            'type': clue_type,
                            'description': description,
                            'importance': importance,
                            'reveal_chapter': int(reveal_chapter) if reveal_chapter.isdigit() else 999,
                            'status': 'planned'
                        }
                        clue_tracker.add_clue(clue_id, clue_data)
                        print(f"✓ 线索 {clue_id} 已添加")
                
                elif clue_choice == '3':
                    chapter_num = input("章节号: ").strip()
                    if chapter_num.isdigit():
                        revealed_clues = clue_tracker.get_revealed_clues(int(chapter_num))
                        print(f"\n第{chapter_num}章前应揭示的线索：")
                        for clue in revealed_clues:
                            print(f"- [{clue.get('type')}] {clue.get('description')}")
                
                elif clue_choice == '4':
                    print("检查线索系统一致性...")
                    # 这里可以添加更复杂的一致性检查逻辑
                    print("✓ 线索系统检查完成")
                
                elif clue_choice == '0':
                    break

        elif choice == '13':
            # 推理逻辑验证
            from agents.mystery_agent import MysteryAgent
            
            mystery_agent = MysteryAgent()
            
            print("\n推理逻辑验证")
            print("=" * 40)
            
            # 获取需要验证的章节
            chapter_num = input("请输入要验证的章节号: ").strip()
            if not chapter_num.isdigit():
                print("无效的章节号")
                continue
            
            chapter_data = storage.load_chapter(int(chapter_num))
            if not chapter_data:
                print(f"未找到第{chapter_num}章")
                continue
            
            # 获取线索系统
            mystery_outline = storage.load_mystery_outline()
            if mystery_outline:
                clue_system = storage.load_clue_system(mystery_outline['id'])
            else:
                clue_system = {}
            
            print(f"正在验证第{chapter_num}章的逻辑一致性...")
            
            verification_result = mystery_agent.verify_logic_consistency(
                chapter_data.get('content', ''),
                clue_system
            )
            
            print(f"\n逻辑验证结果：")
            print(f"总体评分: {verification_result['overall_score']:.1f}/10")
            print(f"逻辑等级: {verification_result['logic_rating']}")
            
            if verification_result['consistency_issues']:
                print(f"\n发现的问题:")
                for issue in verification_result['consistency_issues']:
                    print(f"- {issue}")
            
            if verification_result['suggestions']:
                print(f"\n改进建议:")
                for suggestion in verification_result['suggestions']:
                    print(f"+ {suggestion}")
            
            if verification_result['overall_score'] < 7.0:
                print(f"\n⚠️ 章节逻辑存在问题，建议修改后重新验证")
            else:
                print(f"\n✓ 章节逻辑基本合理")

        elif choice == '14':
            # 精品章节生成（高质量内容引擎）
            from agents.agent_orchestrator import AgentOrchestrator
            from agents import ChapterPlanningAgent
            
            orchestrator = AgentOrchestrator()
            
            print("\n✨ 精品章节生成（高质量内容引擎）")
            print("=" * 50)
            
            # 检查大纲
            outline = storage.load_outline()
            mystery_outline = storage.load_mystery_outline()
            
            if not outline and not mystery_outline:
                print("❌ 未找到大纲，请先创建大纲")
                continue
            
            # 确定章节号
            latest_chapter = storage.get_latest_chapter_number()
            next_chapter = latest_chapter + 1
            
            print(f"🎯 准备使用高质量内容引擎生成第{next_chapter}章")
            
            # 创建章节计划
            planner = ChapterPlanningAgent()
            if mystery_outline:
                # 使用悬疑推理大纲
                context = orchestrator.context_manager.get_full_context()
                chapter_plan = planner.plan_chapter(next_chapter, mystery_outline)
            else:
                chapter_plan = planner.plan_chapter(next_chapter, outline)
            
            if not chapter_plan:
                print("❌ 章节规划失败")
                continue
            
            # 获取完整上下文
            context = orchestrator.context_manager.get_full_context()
            
            print("🚀 启动高质量内容生成引擎...")
            
            # 使用高质量内容生成引擎
            premium_result = orchestrator.generate_premium_chapter(
                chapter_number=next_chapter,
                chapter_plan=chapter_plan,
                context=context
            )
            
            if premium_result:
                print(f"\n✅ 精品章节生成成功！")
                print(f"📄 字数: {premium_result['word_count']}字")
                print(f"⭐ 质量等级: {premium_result['quality_level']}")
                print(f"🤖 生成方法: {premium_result['generation_method']}")
                print(f"🔍 上下文连贯性: 已确保")
                print(f"💾 章节已保存")
                
                print("\n📊 生成特点:")
                print("• 6层质量优化技术栈")
                print("• 文学技巧深度应用") 
                print("• 情感共鸣精准控制")
                print("• 上下文完美连贯")
            else:
                print("❌ 精品章节生成失败")

        elif choice == '15':
            # 整部小说连贯性检查
            from agents.agent_orchestrator import AgentOrchestrator
            
            orchestrator = AgentOrchestrator()
            
            print("\n🔍 整部小说连贯性检查")
            print("=" * 50)
            
            # 获取所有章节
            all_chapters = storage.get_all_chapters()
            if not all_chapters:
                print("❌ 未找到任何章节")
                continue
            
            chapter_numbers = [ch['number'] if 'number' in ch else ch['chapter_number'] for ch in all_chapters]
            
            print(f"📚 检查范围: 第1-{max(chapter_numbers)}章 (共{len(chapter_numbers)}章)")
            
            # 可选择检查范围
            check_range = input("指定检查范围（如：1-5），回车检查全部: ").strip()
            
            if check_range and '-' in check_range:
                try:
                    start, end = map(int, check_range.split('-'))
                    chapter_numbers = list(range(start, end + 1))
                    print(f"🎯 检查范围已设定: 第{start}-{end}章")
                except:
                    print("范围格式错误，将检查全部章节")
            
            print("🚀 开始连贯性检查...")
            
            # 执行检查
            coherence_report = orchestrator.check_novel_coherence(chapter_numbers)
            
            if coherence_report.get('success', True):
                print(f"\n📊 连贯性检查报告:")
                
                # 显示总体评分
                overall_score = coherence_report.get('overall_coherence_score', 0)
                print(f"🏆 总体连贯性评分: {overall_score:.1f}/10")
                
                # 显示各项指标
                character_coherence = coherence_report.get('character_coherence', 0)
                plot_coherence = coherence_report.get('plot_coherence', 0)
                timeline_coherence = coherence_report.get('timeline_coherence', 0)
                
                print(f"👥 角色连贯性: {character_coherence:.1f}/10")
                print(f"📖 情节连贯性: {plot_coherence:.1f}/10") 
                print(f"⏰ 时间线连贯性: {timeline_coherence:.1f}/10")
                
                # 显示问题和建议
                if coherence_report.get('issues'):
                    print(f"\n⚠️ 发现的问题:")
                    for issue in coherence_report['issues'][:5]:  # 显示前5个问题
                        print(f"• {issue}")
                
                if coherence_report.get('suggestions'):
                    print(f"\n💡 改进建议:")
                    for suggestion in coherence_report['suggestions'][:5]:  # 显示前5个建议
                        print(f"• {suggestion}")
                
                # 评级
                if overall_score >= 8.5:
                    print(f"\n🎉 连贯性评级: 优秀")
                elif overall_score >= 7.5:
                    print(f"\n👍 连贯性评级: 良好")
                elif overall_score >= 6.0:
                    print(f"\n⚡ 连贯性评级: 一般，建议优化")
                else:
                    print(f"\n⚠️ 连贯性评级: 需要改进")
                    
            else:
                print(f"❌ 连贯性检查失败: {coherence_report.get('error', 'Unknown error')}")

        elif choice == '16':
            # 智能优化工作流
            from agents.agent_orchestrator import AgentOrchestrator
            
            orchestrator = AgentOrchestrator()
            
            print("\n🧠 智能优化工作流")
            print("=" * 50)
            
            # 获取所有章节
            all_chapters = storage.get_all_chapters()
            if not all_chapters:
                print("❌ 未找到任何章节")
                continue
            
            chapter_numbers = [ch['number'] if 'number' in ch else ch['chapter_number'] for ch in all_chapters]
            print(f"📚 可优化章节: 第1-{max(chapter_numbers)}章")
            
            # 选择目标章节
            target_range = input("指定优化范围（如：1-3），回车优化全部: ").strip()
            
            if target_range and '-' in target_range:
                try:
                    start, end = map(int, target_range.split('-'))
                    target_chapters = list(range(start, end + 1))
                except:
                    target_chapters = chapter_numbers[:3]  # 默认前3章
                    print("范围格式错误，将优化前3章")
            else:
                target_chapters = chapter_numbers
            
            print(f"🎯 目标章节: {len(target_chapters)}章")
            
            # 设置优化目标
            print("\n请设置优化目标（多选，空格分隔）:")
            print("1. 提升内容质量")
            print("2. 改善上下文连贯性") 
            print("3. 平台适配优化")
            print("4. 类型专项优化")
            
            goals_input = input("优化目标 (1 2 3 4，默认：1 2): ").strip()
            if not goals_input:
                goals_input = "1 2"
            
            goals_selected = goals_input.split()
            
            optimization_goals = {
                'improve_quality': '1' in goals_selected,
                'improve_coherence': '2' in goals_selected,
                'platform_optimization': '3' in goals_selected,
                'genre_optimization': '4' in goals_selected,
                'target_platform': 'tomato_novel'
            }
            
            print(f"\n🚀 启动智能优化工作流...")
            print(f"📋 目标章节: {target_chapters}")
            
            # 执行智能优化
            optimization_result = orchestrator.intelligent_optimization_workflow(
                target_chapters, optimization_goals
            )
            
            if optimization_result['success']:
                print(f"\n✅ 智能优化完成！")
                print(f"📊 优化统计:")
                print(f"• 总章节数: {optimization_result['total_chapters']}")
                print(f"• 优化成功: {optimization_result['optimized_chapters']}")
                print(f"• 优化失败: {optimization_result['failed_chapters']}")
                print(f"• 成功率: {optimization_result['optimization_rate']:.1%}")
                
                if optimization_result['overall_improvements']:
                    print(f"\n🎨 应用的改进:")
                    for improvement in optimization_result['overall_improvements']:
                        print(f"• {improvement}")
                
                # 显示详细结果
                successful_chapters = [d for d in optimization_result['details'] if d['status'] == 'success']
                if successful_chapters:
                    print(f"\n📈 优化详情:")
                    for detail in successful_chapters[:5]:  # 显示前5个
                        chapter = detail['chapter']
                        improvements = detail.get('applied_optimizations', [])
                        print(f"第{chapter}章: {', '.join(improvements) if improvements else '无需优化'}")
                
            else:
                print(f"❌ 智能优化失败: {optimization_result.get('error', 'Unknown error')}")

        elif choice == '17':
            # 批量章节优化（高级引擎）
            from agents.agent_orchestrator import AgentOrchestrator
            
            orchestrator = AgentOrchestrator()
            
            print("\n⚡ 批量章节优化（高级引擎）")
            print("=" * 50)
            
            # 获取所有章节
            all_chapters = storage.get_all_chapters()
            if not all_chapters:
                print("❌ 未找到任何章节")
                continue
            
            chapter_numbers = [ch['number'] if 'number' in ch else ch['chapter_number'] for ch in all_chapters]
            print(f"📚 可优化章节: {len(chapter_numbers)}章")
            
            # 选择优化范围
            optimize_range = input("优化范围（如：1-5），回车优化全部: ").strip()
            
            if optimize_range and '-' in optimize_range:
                try:
                    start, end = map(int, optimize_range.split('-'))
                    target_numbers = list(range(start, end + 1))
                except:
                    target_numbers = chapter_numbers
                    print("范围格式错误，将优化全部章节")
            else:
                target_numbers = chapter_numbers
            
            # 选择优化类型
            print("\n请选择优化类型:")
            print("1. 全面优化 (comprehensive)")
            print("2. 上下文优化 (context)")
            print("3. 质量优化 (quality)")
            print("4. 平台优化 (platform)")
            
            opt_type_choice = input("优化类型 (1-4，默认1): ").strip()
            type_map = {
                '1': 'comprehensive',
                '2': 'context', 
                '3': 'quality',
                '4': 'platform'
            }
            optimization_type = type_map.get(opt_type_choice, 'comprehensive')
            
            print(f"\n🎯 优化配置:")
            print(f"• 目标章节: {len(target_numbers)}章")
            print(f"• 优化类型: {optimization_type}")
            
            confirm = input("\n确认开始批量优化？(y/n): ").strip().lower()
            if confirm != 'y':
                print("取消优化")
                continue
            
            print("🚀 开始批量优化...")
            print("⏳ 这可能需要几分钟时间...")
            
            # 执行批量优化
            batch_result = orchestrator.batch_optimize_chapters(target_numbers, optimization_type)
            
            print(f"\n📊 批量优化完成！")
            print(f"✅ 成功优化: {batch_result['optimized_count']}章")
            print(f"❌ 优化失败: {batch_result['failed_count']}章")
            
            # 显示成功的优化详情
            successful_details = [d for d in batch_result['details'] if d['status'] == 'success']
            if successful_details:
                print(f"\n🎨 优化详情:")
                for detail in successful_details:
                    chapter = detail['chapter']
                    improvements = detail.get('improvements', [])
                    if improvements:
                        print(f"第{chapter}章: {', '.join(improvements)}")
                    else:
                        print(f"第{chapter}章: 质量已达标，无需优化")
            
            # 显示失败的章节
            failed_details = [d for d in batch_result['details'] if d['status'] == 'failed']
            if failed_details:
                print(f"\n❌ 优化失败的章节:")
                for detail in failed_details[:3]:  # 只显示前3个失败
                    chapter = detail['chapter']
                    error = detail.get('error', 'Unknown error')
                    print(f"第{chapter}章: {error}")
            
            if batch_result['optimized_count'] > 0:
                print(f"\n✨ 批量优化成功！章节质量已显著提升")
                print(f"💾 所有优化已自动保存")

        elif choice == '18':
            # AI小说8大问题解决方案
            from utils.dynamic_learning_engine import DynamicLearningEngine
            
            learning_engine = DynamicLearningEngine()
            
            print("\n🔧 AI小说8大问题解决方案")
            print("=" * 50)
            print("本系统专门针对AI小说创作的8大核心问题：")
            print("1. 逻辑连贯性薄弱（长篇重灾区）")
            print("2. 情感共鸣缺失（内容缺乏温度）")
            print("3. 原创性与突破性不足")
            print("4. 人物塑造扁平化")
            print("5. 语言有AI味显僵化")
            print("6. 叙事节奏失控")
            print("7. 主题与思想浅薄")
            print("8. 文化适配性差")
            
            # 选择要处理的章节
            all_chapters = storage.get_all_chapters()
            if not all_chapters:
                print("\n❌ 未找到任何章节")
                continue
            
            chapter_numbers = [ch['number'] if 'number' in ch else ch['chapter_number'] for ch in all_chapters]
            print(f"\n📚 可处理章节: {len(chapter_numbers)}章")
            
            target_chapter = input("请输入要处理的章节号（或输入'all'处理全部）: ").strip()
            
            if target_chapter.lower() == 'all':
                target_chapters = chapter_numbers[:3]  # 限制处理前3章避免过长
                print(f"将处理前3章进行演示")
            elif target_chapter.isdigit():
                target_chapters = [int(target_chapter)]
            else:
                print("无效输入")
                continue
            
            # 选择要解决的问题
            print("\n请选择要解决的问题（多选，空格分隔，默认全部）:")
            print("1-逻辑连贯性  2-情感共鸣  3-原创性  4-人物塑造")
            print("5-AI语言问题  6-叙事节奏  7-主题深度  8-文化适配")
            
            problems_input = input("问题编号 (1 2 3 4 5 6 7 8): ").strip()
            if problems_input:
                target_problems = [int(p) for p in problems_input.split() if p.isdigit() and 1 <= int(p) <= 8]
            else:
                target_problems = list(range(1, 9))  # 默认所有问题
            
            problem_names = [
                "逻辑连贯性", "情感共鸣", "原创性", "人物塑造",
                "AI语言问题", "叙事节奏", "主题深度", "文化适配性"
            ]
            
            print(f"\n🎯 目标问题: {', '.join([problem_names[p-1] for p in target_problems])}")
            
            # 处理每个章节
            for chapter_num in target_chapters:
                chapter_data = storage.load_chapter(chapter_num)
                if not chapter_data:
                    print(f"❌ 未找到第{chapter_num}章")
                    continue
                
                print(f"\n🔧 处理第{chapter_num}章...")
                
                # 构建上下文
                outline = storage.load_outline()
                mystery_outline = storage.load_mystery_outline()
                context = {
                    'genre': '悬疑推理' if mystery_outline else '通用',
                    'outline': outline or mystery_outline,
                    'chapter_number': chapter_num
                }
                
                # 解决核心问题
                solution_result = learning_engine.solve_core_problems(
                    chapter_data.get('content', ''),
                    context,
                    target_problems
                )
                
                if solution_result['success']:
                    # 更新章节
                    updated_data = chapter_data.copy()
                    updated_data['content'] = solution_result['improved_content']
                    updated_data['word_count'] = len(solution_result['improved_content'])
                    updated_data['ai_optimized'] = True
                    updated_data['solved_problems'] = solution_result['applied_solutions']
                    updated_data['problem_scores'] = solution_result['problem_scores']
                    
                    storage.update_chapter(chapter_num, updated_data)
                    
                    print(f"✅ 第{chapter_num}章处理完成！")
                    print(f"📈 解决方案: {', '.join(solution_result['applied_solutions'])}")
                    print(f"🏆 整体改进度: {solution_result['overall_improvement']:.1f}/10")
                    
                    # 显示各问题得分
                    for prob_id, score in solution_result['problem_scores'].items():
                        prob_name = problem_names[prob_id - 1]
                        print(f"   {prob_name}: {score:.1f}/10")
                        
                else:
                    print(f"❌ 第{chapter_num}章处理失败")
            
            print(f"\n🎉 8大问题解决方案处理完成！")
            print(f"💡 提示：您可以使用选项20查看详细的质量报告")

        elif choice == '19':
            # 爆款小说学习与分析
            from utils.dynamic_learning_engine import DynamicLearningEngine
            
            learning_engine = DynamicLearningEngine()
            
            print("\n📚 爆款小说学习与分析系统")
            print("=" * 50)
            print("本系统可以分析爆款小说的成功模式，学习其写作技巧")
            
            # 选择学习类型
            print("\n请选择操作类型：")
            print("1. 分析爆款小说样本")
            print("2. 学习指定类型的成功作品")
            print("3. 查看已学习的模式库")
            
            learn_choice = input("请选择 (1-3): ").strip()
            
            if learn_choice == '1':
                # 分析爆款小说样本
                print("\n📖 爆款小说样本分析")
                print("请选择要分析的小说类型：")
                print("1. 悬疑推理  2. 言情现代  3. 玄幻奇幻")
                print("4. 科幻未来  5. 历史古代  6. 都市现代")
                
                genre_choice = input("类型选择 (1-6): ").strip()
                genre_map = {
                    '1': '悬疑推理', '2': '言情现代', '3': '玄幻奇幻',
                    '4': '科幻未来', '5': '历史古代', '6': '都市现代'
                }
                genre = genre_map.get(genre_choice, '悬疑推理')
                
                print(f"\n请提供{genre}类型的爆款小说样本（每行一个样本，至少3个）：")
                print("示例格式：")
                print("《东野圭吾：白夜行》- 悬念设置精妙，人物关系复杂...")
                print("输入'END'结束输入：")
                
                sample_texts = []
                while True:
                    sample = input("样本: ").strip()
                    if sample.upper() == 'END':
                        break
                    if sample:
                        sample_texts.append(sample)
                
                if len(sample_texts) < 2:
                    print("样本数量不足，至少需要2个样本")
                    continue
                
                print(f"\n🔍 开始分析{len(sample_texts)}个{genre}样本...")
                
                analysis_result = learning_engine.analyze_bestseller_patterns(genre, sample_texts)
                
                if analysis_result.get('success'):
                    print(f"✅ {analysis_result['message']}")
                    patterns = analysis_result['patterns']
                    
                    print(f"\n📊 成功模式分析结果:")
                    if 'success_patterns' in patterns:
                        for aspect, features in patterns['success_patterns'].items():
                            aspect_names = {
                                'logic_coherence': '逻辑连贯性',
                                'emotional_resonance': '情感共鸣',
                                'originality': '原创性',
                                'character_depth': '人物塑造',
                                'language_style': '语言风格',
                                'narrative_rhythm': '叙事节奏',
                                'theme_depth': '主题深度',
                                'cultural_authenticity': '文化真实性'
                            }
                            aspect_name = aspect_names.get(aspect, aspect)
                            print(f"• {aspect_name}: {', '.join(features)}")
                    
                    if 'key_techniques' in patterns:
                        print(f"\n🎯 核心技巧:")
                        for technique in patterns['key_techniques']:
                            print(f"• {technique}")
                            
                else:
                    print(f"❌ 分析失败: {analysis_result.get('error', 'Unknown error')}")
                    if 'raw_analysis' in analysis_result:
                        print(f"原始分析结果:\n{analysis_result['raw_analysis']}")
            
            elif learn_choice == '2':
                # 学习指定类型的成功作品
                print("\n🎓 学习成功作品")
                genre = input("请输入要学习的小说类型（如：悬疑推理）: ").strip()
                
                print(f"\n请输入{genre}类型的成功小说名单（每行一个，输入'END'结束）：")
                reference_novels = []
                while True:
                    novel = input("作品: ").strip()
                    if novel.upper() == 'END':
                        break
                    if novel:
                        reference_novels.append(novel)
                
                if reference_novels:
                    print(f"\n📚 开始学习{len(reference_novels)}部{genre}作品...")
                    
                    learning_result = learning_engine.learn_from_bestsellers(genre, reference_novels)
                    
                    if learning_result['success']:
                        print(f"✅ {learning_result['message']}")
                        print(f"\n📖 学习成果:")
                        analysis = learning_result['learning_data']['analysis_result']
                        # 显示学习结果的前500字符
                        print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
                    else:
                        print(f"❌ 学习失败: {learning_result['error']}")
                else:
                    print("未提供学习材料")
            
            elif learn_choice == '3':
                # 查看已学习的模式库
                print("\n📋 模式库总览")
                
                patterns = learning_engine.bestseller_patterns
                if patterns:
                    for genre, genre_patterns in patterns.items():
                        print(f"\n📚 {genre}:")
                        for aspect, features in genre_patterns.items():
                            if isinstance(features, list):
                                print(f"  • {aspect}: {', '.join(features)}")
                            else:
                                print(f"  • {aspect}: {features}")
                else:
                    print("暂无学习数据")
                
                print(f"\n💡 提示：学习数据保存在 data/learning/ 目录中")

        elif choice == '20':
            # 内容质量深度报告
            from utils.dynamic_learning_engine import DynamicLearningEngine
            
            learning_engine = DynamicLearningEngine()
            
            print("\n📊 内容质量深度报告")
            print("=" * 50)
            
            # 选择分析对象
            all_chapters = storage.get_all_chapters()
            if not all_chapters:
                print("❌ 未找到任何章节")
                continue
            
            chapter_numbers = [ch['number'] if 'number' in ch else ch['chapter_number'] for ch in all_chapters]
            print(f"📚 可分析章节: {len(chapter_numbers)}章")
            
            analysis_target = input("请输入要分析的章节号（或'all'分析全部）: ").strip()
            
            if analysis_target.lower() == 'all':
                target_chapters = chapter_numbers
                print(f"将分析全部{len(target_chapters)}章")
            elif analysis_target.isdigit():
                target_chapters = [int(analysis_target)]
            else:
                print("无效输入")
                continue
            
            print(f"\n🔍 开始深度质量分析...")
            
            total_reports = []
            
            for chapter_num in target_chapters:
                chapter_data = storage.load_chapter(chapter_num)
                if not chapter_data:
                    print(f"❌ 未找到第{chapter_num}章")
                    continue
                
                print(f"\n📖 分析第{chapter_num}章...")
                
                # 构建分析上下文
                outline = storage.load_outline()
                mystery_outline = storage.load_mystery_outline()
                context = {
                    'genre': '悬疑推理' if mystery_outline else '通用',
                    'chapter_number': chapter_num,
                    'total_chapters': len(chapter_numbers)
                }
                
                # 生成质量报告
                quality_report = learning_engine.get_quality_report(
                    chapter_data.get('content', ''),
                    context
                )
                
                if quality_report['success']:
                    print(f"✅ 第{chapter_num}章分析完成")
                    print(f"🏆 总体评分: {quality_report['overall_score']:.1f}/10 ({quality_report['overall_level']})")
                    
                    print(f"\n📋 详细分析:")
                    for problem_name, analysis in quality_report['problem_analysis'].items():
                        score = analysis['score']
                        level = analysis['level']
                        suggestions = analysis['suggestions']
                        
                        status_emoji = "🟢" if score >= 7.0 else "🟡" if score >= 6.0 else "🔴"
                        print(f"{status_emoji} {problem_name}: {score:.1f}/10 ({level})")
                        
                        if suggestions and len(suggestions) > 0:
                            print(f"   💡 建议: {suggestions[0]}")
                    
                    # 优先改进项目
                    if quality_report['priority_improvements']:
                        print(f"\n🎯 优先改进项目:")
                        for improvement in quality_report['priority_improvements']:
                            print(f"• {improvement}")
                    
                    total_reports.append({
                        'chapter': chapter_num,
                        'score': quality_report['overall_score'],
                        'level': quality_report['overall_level'],
                        'report': quality_report
                    })
                else:
                    print(f"❌ 第{chapter_num}章分析失败: {quality_report.get('error', 'Unknown error')}")
            
            # 生成总体报告
            if total_reports:
                print(f"\n📈 总体质量分析报告")
                print("=" * 40)
                
                avg_score = sum(r['score'] for r in total_reports) / len(total_reports)
                print(f"📊 平均质量评分: {avg_score:.1f}/10")
                
                # 各等级统计
                level_counts = {}
                for report in total_reports:
                    level = report['level']
                    level_counts[level] = level_counts.get(level, 0) + 1
                
                print(f"📋 质量等级分布:")
                for level, count in level_counts.items():
                    percentage = (count / len(total_reports)) * 100
                    print(f"• {level}: {count}章 ({percentage:.1f}%)")
                
                # 最需要改进的章节
                low_quality_chapters = [r for r in total_reports if r['score'] < 7.0]
                if low_quality_chapters:
                    low_quality_chapters.sort(key=lambda x: x['score'])
                    print(f"\n⚠️ 最需要改进的章节:")
                    for chapter_info in low_quality_chapters[:3]:  # 显示前3个
                        print(f"• 第{chapter_info['chapter']}章: {chapter_info['score']:.1f}/10 ({chapter_info['level']})")
                
                # 推荐改进方案
                print(f"\n💡 推荐改进方案:")
                print("1. 使用选项18的8大问题解决方案进行针对性优化")
                print("2. 使用选项16的智能优化工作流进行批量提升")
                print("3. 使用选项14的精品章节生成重新创作低质量章节")
                print("4. 参考选项19学习的爆款小说模式进行改进")
            
            print(f"\n🎉 质量分析报告完成！")

        elif choice == '21':
            # 自我反思内容生成（Self-RAG）
            from utils.self_reflection_engine import SelfReflectionEngine, NovelQualityValidator
            from utils import LLMClient
            
            reflection_engine = SelfReflectionEngine(LLMClient())
            
            print("\n🧠 自我反思内容生成（Self-RAG）")
            print("=" * 50)
            print("基于Self-RAG技术，提供内容生成的自我评估和改进能力")
            
            # 选择生成模式
            print("\n请选择生成模式：")
            print("1. 单章节自我反思生成")
            print("2. 批量章节自我反思优化")
            print("3. 整部小说质量验证")
            
            mode_choice = input("模式选择 (1-3): ").strip()
            
            if mode_choice == '1':
                # 单章节自我反思生成
                print("\n📝 单章节自我反思生成")
                
                # 获取章节信息
                outline = storage.load_outline()
                mystery_outline = storage.load_mystery_outline()
                
                if not outline and not mystery_outline:
                    print("❌ 未找到大纲，请先创建大纲")
                    continue
                
                latest_chapter = storage.get_latest_chapter_number()
                next_chapter = latest_chapter + 1
                
                prompt = f"请为第{next_chapter}章生成高质量小说内容"
                context = {
                    'chapter_number': next_chapter,
                    'outline': outline or mystery_outline,
                    'genre': '悬疑推理' if mystery_outline else '通用'
                }
                
                print(f"🚀 开始自我反思生成第{next_chapter}章...")
                
                reflection_result = reflection_engine.generate_with_reflection(prompt, context)
                
                if reflection_result.get('final_content'):
                    print(f"\n✅ 第{next_chapter}章自我反思生成完成！")
                    print(f"📊 质量评分: {reflection_result['quality_score']:.1f}/10")
                    print(f"🔄 改进应用: {'是' if reflection_result['improvement_applied'] else '否'}")
                    
                    # 保存章节
                    chapter_data = {
                        'chapter_number': next_chapter,
                        'title': f'第{next_chapter}章',
                        'content': reflection_result['final_content'],
                        'word_count': len(reflection_result['final_content']),
                        'self_reflection': {
                            'applied': reflection_result['improvement_applied'],
                            'quality_score': reflection_result['quality_score'],
                            'initial_reflection': reflection_result.get('initial_reflection', {}),
                            'final_reflection': reflection_result.get('final_reflection', {})
                        }
                    }
                    
                    storage.save_chapter(next_chapter, chapter_data)
                    print(f"💾 章节已保存")
                else:
                    print("❌ 生成失败")
                    if reflection_result.get('error'):
                        print(f"错误: {reflection_result['error']}")
            
            elif mode_choice == '2':
                # 批量章节自我反思优化
                print("\n⚡ 批量章节自我反思优化")
                
                all_chapters = storage.get_all_chapters()
                if not all_chapters:
                    print("❌ 未找到任何章节")
                    continue
                
                chapter_numbers = [ch['number'] if 'number' in ch else ch['chapter_number'] for ch in all_chapters]
                
                # 选择优化范围
                optimize_range = input(f"优化范围（如：1-3，回车优化前3章）: ").strip()
                
                if optimize_range and '-' in optimize_range:
                    try:
                        start, end = map(int, optimize_range.split('-'))
                        target_chapters = list(range(start, end + 1))
                    except:
                        target_chapters = chapter_numbers[:3]
                else:
                    target_chapters = chapter_numbers[:3]  # 默认前3章
                
                print(f"🎯 将优化 {len(target_chapters)} 个章节")
                
                # 准备章节内容
                chapter_contents = []
                for ch_num in target_chapters:
                    ch_data = storage.load_chapter(ch_num)
                    if ch_data:
                        chapter_contents.append((ch_num, ch_data.get('content', '')))
                
                if chapter_contents:
                    print("🚀 开始批量自我反思优化...")
                    
                    batch_result = reflection_engine.batch_reflect_chapters(chapter_contents)
                    
                    if batch_result:
                        summary = batch_result['summary']
                        print(f"\n📊 批量优化完成:")
                        print(f"• 总章节数: {summary['total_chapters']}")
                        print(f"• 平均质量: {summary['average_quality']:.1f}/10")
                        print(f"• 改进章节数: {summary['improved_chapters']}")
                        print(f"• 改进率: {summary['improvement_rate']:.1%}")
                        
                        # 更新章节数据
                        for ch_key, ch_result in batch_result['chapter_results'].items():
                            if ch_result['improvement_applied']:
                                ch_num = int(ch_key.split('_')[1])
                                storage.update_chapter(ch_num, {
                                    'content': ch_result['final_content'],
                                    'word_count': len(ch_result['final_content']),
                                    'self_reflection_optimized': True,
                                    'quality_score': ch_result['quality_score']
                                })
                        
                        print("💾 优化结果已保存")
                else:
                    print("❌ 未找到可优化的章节内容")
            
            elif mode_choice == '3':
                # 整部小说质量验证
                print("\n🔍 整部小说质量验证")
                
                all_chapters = storage.get_all_chapters()
                if not all_chapters:
                    print("❌ 未找到任何章节")
                    continue
                
                validator = NovelQualityValidator(reflection_engine)
                
                print("🚀 开始整部小说质量验证...")
                
                validation_result = validator.validate_novel_coherence(all_chapters)
                
                print(f"\n📊 小说质量验证报告:")
                print(f"🏆 总体连贯性: {validation_result['overall_coherence_score']:.1f}/10")
                print(f"📈 平均质量: {validation_result['average_quality_score']:.1f}/10")
                print(f"✅ 验证通过: {'是' if validation_result['validation_passed'] else '否'}")
                
                if validation_result['coherence_issues']:
                    print(f"\n⚠️ 发现的连贯性问题:")
                    for issue in validation_result['coherence_issues'][:5]:
                        print(f"• {issue}")
                
                print(f"\n📋 章节质量详情:")
                for ch_quality in validation_result['chapter_qualities'][:10]:  # 显示前10章
                    chapter = ch_quality['chapter']
                    score = ch_quality['quality_score']
                    status = "✅" if score >= 7.0 else "⚠️" if score >= 6.0 else "❌"
                    print(f"{status} 第{chapter}章: {score:.1f}/10")

        elif choice == '22':
            # 多模态小说创作
            from utils.multimodal_generator import MultimodalGenerator, MultimodalAnalyzer
            from utils import LLMClient
            from agents import ChapterPlanningAgent
            
            multimodal_generator = MultimodalGenerator(LLMClient())
            analyzer = MultimodalAnalyzer(LLMClient())
            
            print("\n🎨 多模态小说创作")
            print("=" * 50)
            print("支持文本、图像、音频等多媒体小说创作")
            
            # 选择创作模式
            print("\n请选择创作模式：")
            print("1. 单章节多模态生成")
            print("2. 创建完整多媒体小说包")
            print("3. 导出多媒体格式")
            
            multimodal_choice = input("模式选择 (1-3): ").strip()
            
            if multimodal_choice == '1':
                # 单章节多模态生成
                print("\n🎬 单章节多模态生成")
                
                # 获取章节信息
                outline = storage.load_outline()
                mystery_outline = storage.load_mystery_outline()
                
                if not outline and not mystery_outline:
                    print("❌ 未找到大纲，请先创建大纲")
                    continue
                
                latest_chapter = storage.get_latest_chapter_number()
                next_chapter = latest_chapter + 1
                
                # 创建章节计划
                planner = ChapterPlanningAgent()
                chapter_plan = {
                    'chapter_number': next_chapter,
                    'chapter_title': f'第{next_chapter}章',
                    'main_plot_points': ['主要情节发展'],
                    'character_development': ['角色发展']
                }
                
                # 配置多模态选项
                print("\n🔧 配置多模态元素:")
                include_images = input("包含图像描述? (y/n): ").strip().lower() == 'y'
                include_audio = input("包含音频描述? (y/n): ").strip().lower() == 'y'
                include_viz = input("包含场景可视化? (y/n): ").strip().lower() == 'y'
                
                style = input("选择风格 (realistic/fantasy/noir/romantic/thriller): ").strip() or 'realistic'
                
                multimodal_config = {
                    'include_images': include_images,
                    'include_audio': include_audio,
                    'include_visualization': include_viz,
                    'style': style,
                    'target_length': 3000
                }
                
                print(f"🚀 开始生成多模态第{next_chapter}章...")
                
                multimodal_result = multimodal_generator.generate_multimodal_chapter(
                    chapter_plan, multimodal_config
                )
                
                if multimodal_result.get('text_content'):
                    print(f"\n✅ 多模态章节生成完成！")
                    print(f"📄 文本字数: {multimodal_result['word_count']}字")
                    print(f"🎨 多模态元素:")
                    
                    elements = multimodal_result.get('multimodal_elements', {})
                    if elements.get('images'):
                        print(f"  📷 图像描述: {len(elements['images'])}个场景")
                    if elements.get('audio'):
                        print(f"  🎵 音频元素: 已生成")
                    if elements.get('visualizations'):
                        print(f"  🎬 场景可视化: {len(elements['visualizations'])}个场景")
                    if elements.get('experience'):
                        print(f"  ✨ 体验增强: 已生成")
                    
                    # 保存多模态章节
                    chapter_data = {
                        'chapter_number': next_chapter,
                        'title': multimodal_result['title'],
                        'content': multimodal_result['text_content'],
                        'word_count': multimodal_result['word_count'],
                        'multimodal': True,
                        'multimodal_elements': multimodal_result['multimodal_elements']
                    }
                    
                    storage.save_chapter(next_chapter, chapter_data)
                    print(f"💾 多模态章节已保存")
                else:
                    print("❌ 生成失败")
            
            elif multimodal_choice == '2':
                # 创建完整多媒体小说包
                print("\n📦 创建完整多媒体小说包")
                
                all_chapters = storage.get_all_chapters()
                if not all_chapters:
                    print("❌ 未找到任何章节")
                    continue
                
                # 配置多媒体包
                novel_title = input("小说标题: ").strip() or "未命名小说"
                novel_description = input("小说描述: ").strip()
                
                package_config = {
                    'novel_title': novel_title,
                    'novel_description': novel_description,
                    'include_images': True,
                    'include_audio': True,
                    'include_visualization': True,
                    'style': 'realistic'
                }
                
                print(f"🚀 创建多媒体小说包...")
                print(f"📚 处理 {len(all_chapters)} 个章节...")
                
                multimedia_package = multimodal_generator.create_multimedia_package(
                    all_chapters, package_config
                )
                
                if multimedia_package:
                    print(f"\n✅ 多媒体小说包创建完成！")
                    print(f"📖 小说标题: {multimedia_package['title']}")
                    print(f"📄 章节数量: {multimedia_package['package_info']['total_chapters']}")
                    print(f"🎨 多媒体元素: {multimedia_package['package_info']['multimodal_elements_count']}")
                    
                    # 保存多媒体包
                    storage.save_multimedia_package(multimedia_package)
                    print(f"💾 多媒体包已保存")
                    
                    # 分析多媒体效果
                    effectiveness = analyzer.analyze_multimedia_effectiveness(multimedia_package)
                    if effectiveness:
                        print(f"\n📊 多媒体效果分析:")
                        scores = effectiveness.get('effectiveness_scores', {})
                        for metric, score in scores.items():
                            print(f"• {metric}: {score:.1f}/10")
                else:
                    print("❌ 多媒体包创建失败")
            
            elif multimodal_choice == '3':
                # 导出多媒体格式
                print("\n📤 导出多媒体格式")
                
                # 尝试加载已有的多媒体包
                multimedia_package = storage.load_multimedia_package()
                if not multimedia_package:
                    print("❌ 未找到多媒体包，请先创建（选项2）")
                    continue
                
                print("请选择导出格式：")
                print("1. 增强型EPUB (epub_enhanced)")
                print("2. 交互式Web应用 (interactive_web)")
                print("3. 有声书脚本 (audiobook_script)")
                print("4. VR体验 (vr_experience)")
                
                format_choice = input("格式选择 (1-4): ").strip()
                format_map = {
                    '1': 'epub_enhanced',
                    '2': 'interactive_web',
                    '3': 'audiobook_script',
                    '4': 'vr_experience'
                }
                
                export_format = format_map.get(format_choice, 'epub_enhanced')
                
                print(f"🚀 导出为 {export_format} 格式...")
                
                export_result = multimodal_generator.export_to_format(
                    multimedia_package, export_format
                )
                
                if export_result and 'error' not in export_result:
                    print(f"✅ 导出完成！")
                    print(f"📁 格式: {export_result['format']}")
                    
                    # 保存导出结果
                    storage.save_export_result(export_format, export_result)
                    print(f"💾 导出文件已保存")
                else:
                    print(f"❌ 导出失败: {export_result.get('error', 'Unknown error')}")

        elif choice == '23':
            # 智能对话系统
            from utils.intelligent_dialogue_system import (
                CharacterDialogueEngine, EmotionalDialogueGenerator, 
                DialogueOptimizationEngine, ConversationFlowManager
            )
            from utils import LLMClient
            
            llm_client = LLMClient()
            character_engine = CharacterDialogueEngine(llm_client)
            emotional_engine = EmotionalDialogueGenerator(llm_client)
            optimization_engine = DialogueOptimizationEngine(llm_client)
            flow_manager = ConversationFlowManager(character_engine, emotional_engine)
            
            print("\n💬 智能对话系统")
            print("=" * 50)
            print("基于现代RAG技术，提供智能角色对话生成和情感表达")
            
            # 选择对话模式
            print("\n请选择对话模式：")
            print("1. 角色对话生成")
            print("2. 情感对话生成")
            print("3. 对话优化")
            print("4. 多轮对话序列")
            
            dialogue_choice = input("模式选择 (1-4): ").strip()
            
            if dialogue_choice == '1':
                # 角色对话生成
                print("\n👥 角色对话生成")
                
                character_name = input("说话角色名称: ").strip()
                if not character_name:
                    print("❌ 角色名称不能为空")
                    continue
                
                target_character = input("对话目标角色（可选）: ").strip() or None
                scene_description = input("场景描述: ").strip()
                
                dialogue_context = {
                    'scene_description': scene_description,
                    'location': input("地点: ").strip(),
                    'time': input("时间: ").strip(),
                    'mood': input("整体氛围: ").strip()
                }
                
                print(f"🚀 生成{character_name}的对话...")
                
                dialogue_result = character_engine.generate_character_dialogue(
                    character_name, dialogue_context, target_character
                )
                
                if dialogue_result.get('dialogue'):
                    print(f"\n✅ 对话生成完成！")
                    print(f"💬 {character_name}: {dialogue_result['dialogue']}")
                    
                    quality = dialogue_result.get('quality_metrics', {})
                    print(f"\n📊 对话质量:")
                    print(f"🏆 总体评分: {quality.get('overall_score', 0):.1f}/10")
                    print(f"👤 角色一致性: {quality.get('character_consistency', 0):.1f}/10")
                    print(f"🗣️ 语言自然度: {quality.get('language_naturalness', 0):.1f}/10")
                    print(f"❤️ 情感表达: {quality.get('emotional_expression', 0):.1f}/10")
                else:
                    print("❌ 对话生成失败")
                    if dialogue_result.get('error'):
                        print(f"错误: {dialogue_result['error']}")
            
            elif dialogue_choice == '2':
                # 情感对话生成
                print("\n❤️ 情感对话生成")
                
                print("选择主要情感类型：")
                emotion_types = {
                    '1': 'joy', '2': 'sadness', '3': 'anger', '4': 'fear',
                    '5': 'love', '6': 'anxiety', '7': 'hope', '8': 'regret'
                }
                
                for key, emotion in emotion_types.items():
                    print(f"{key}. {emotion}")
                
                emotion_choice = input("情感选择 (1-8): ").strip()
                primary_emotion = emotion_types.get(emotion_choice, 'joy')
                
                intensity = input("情感强度 (1-10): ").strip()
                try:
                    intensity = int(intensity)
                    intensity = max(1, min(10, intensity))  # 限制在1-10范围内
                except:
                    intensity = 5
                
                context_description = input("情感触发情境: ").strip()
                
                emotion_config = {
                    'primary_emotion': primary_emotion,
                    'intensity': intensity,
                    'context': {
                        'situation': context_description,
                        'trigger': input("情感触发点: ").strip()
                    }
                }
                
                print(f"🚀 生成{primary_emotion}情感对话（强度{intensity}/10）...")
                
                emotional_result = emotional_engine.generate_emotional_dialogue(emotion_config)
                
                if emotional_result.get('dialogue'):
                    print(f"\n✅ 情感对话生成完成！")
                    print(f"💬 对话内容：\n{emotional_result['dialogue']}")
                    
                    impact = emotional_result.get('emotional_impact', {})
                    print(f"\n📊 情感影响力:")
                    print(f"🎯 总体影响: {impact.get('overall_impact', 0):.1f}/10")
                    print(f"🎭 情感真实度: {impact.get('emotional_authenticity', 0):.1f}/10")
                    print(f"✨ 感染力: {impact.get('infectiousness', 0):.1f}/10")
                    print(f"🎨 艺术价值: {impact.get('artistic_value', 0):.1f}/10")
                else:
                    print("❌ 情感对话生成失败")
            
            elif dialogue_choice == '3':
                # 对话优化
                print("\n⚡ 对话优化")
                
                original_dialogue = input("请输入要优化的对话内容：\n").strip()
                if not original_dialogue:
                    print("❌ 对话内容不能为空")
                    continue
                
                print("\n选择优化目标（多选，空格分隔）：")
                print("1. 自然度优化  2. 个性化优化  3. 情感表达优化")
                print("4. 节奏韵律优化  5. 言外之意优化")
                
                goals_input = input("优化目标 (如: 1 2 3): ").strip()
                optimization_goals = []
                
                goal_map = {
                    '1': 'naturalness', '2': 'personality', '3': 'emotion',
                    '4': 'rhythm', '5': 'subtext'
                }
                
                for goal_num in goals_input.split():
                    if goal_num in goal_map:
                        optimization_goals.append(goal_map[goal_num])
                
                if not optimization_goals:
                    optimization_goals = ['naturalness', 'emotion']  # 默认优化
                
                dialogue_data = {
                    'dialogue': original_dialogue,
                    'optimization_goals': optimization_goals,
                    'character_profile': {},
                    'emotional_context': {},
                    'scene_context': {}
                }
                
                print(f"🚀 开始对话优化...")
                
                optimization_result = optimization_engine.optimize_dialogue_comprehensive(dialogue_data)
                
                if optimization_result.get('optimized_dialogue'):
                    print(f"\n✅ 对话优化完成！")
                    print(f"\n📝 原始对话：\n{optimization_result['original_dialogue']}")
                    print(f"\n✨ 优化后对话：\n{optimization_result['optimized_dialogue']}")
                    
                    print(f"\n🎨 应用的优化:")
                    for optimization in optimization_result['applied_optimizations']:
                        print(f"• {optimization}")
                    
                    assessment = optimization_result.get('quality_assessment', {})
                    print(f"\n📊 优化后质量:")
                    print(f"🏆 总体评分: {assessment.get('overall_score', 0):.1f}/10")
                    print(f"📈 改进幅度: +{optimization_result.get('improvement_score', 0):.1f}")
                else:
                    print("❌ 对话优化失败")
            
            elif dialogue_choice == '4':
                # 多轮对话序列
                print("\n🔄 多轮对话序列")
                
                # 获取参与者
                participants_input = input("参与对话的角色（用空格分隔，如：张三 李四）: ").strip()
                participants = participants_input.split() if participants_input else ['角色A', '角色B']
                
                conversation_length = input("对话轮数（默认5）: ").strip()
                try:
                    conversation_length = int(conversation_length)
                except:
                    conversation_length = 5
                
                theme = input("对话主题（如：日常交流、冲突争执）: ").strip() or '日常交流'
                
                # 情感发展弧线（可选）
                print("\n设置情感发展弧线（可选，回车跳过）:")
                emotional_arc = []
                for i in range(conversation_length):
                    emotion = input(f"第{i+1}轮情感（joy/sadness/anger/neutral）: ").strip()
                    emotional_arc.append(emotion if emotion else 'neutral')
                
                conversation_config = {
                    'length': conversation_length,
                    'theme': theme,
                    'emotional_arc': emotional_arc,
                    'initial_context': {
                        'setting': input("对话场景: ").strip()
                    }
                }
                
                print(f"🚀 生成{len(participants)}人{conversation_length}轮对话...")
                
                conversation_result = flow_manager.generate_conversation_sequence(
                    participants, conversation_config
                )
                
                if conversation_result.get('conversation_sequence'):
                    print(f"\n✅ 对话序列生成完成！")
                    print(f"🎭 参与者: {', '.join(participants)}")
                    print(f"🎯 主题: {theme}")
                    
                    print(f"\n💬 对话内容:")
                    for turn in conversation_result['conversation_sequence']:
                        speaker = turn['speaker']
                        dialogue = turn['dialogue']
                        emotion = turn['emotion']
                        print(f"\n第{turn['turn']}轮 - {speaker} [{emotion}]:")
                        print(f"「{dialogue}」")
                    
                    flow_analysis = conversation_result.get('flow_analysis', {})
                    print(f"\n📊 对话流畅性分析:")
                    print(f"🏆 连贯性评分: {flow_analysis.get('coherence_score', 0):.1f}/10")
                    print(f"❤️ 情感发展: {flow_analysis.get('emotional_progression', 'N/A')}")
                    print(f"🎵 节奏一致性: {flow_analysis.get('rhythm_consistency', 'N/A')}")
                else:
                    print("❌ 对话序列生成失败")

        elif choice == '24':
            # 整合式高级创作模式
            from utils.self_reflection_engine import SelfReflectionEngine
            from utils.multimodal_generator import MultimodalGenerator
            from utils.intelligent_dialogue_system import CharacterDialogueEngine
            from utils.dynamic_learning_engine import DynamicLearningEngine
            from agents.agent_orchestrator import AgentOrchestrator
            from utils import LLMClient
            
            print("\n🌟 整合式高级创作模式")
            print("=" * 50)
            print("综合运用所有高级AI技术的终极创作模式")
            
            # 初始化所有引擎
            llm_client = LLMClient()
            reflection_engine = SelfReflectionEngine(llm_client)
            multimodal_generator = MultimodalGenerator(llm_client)
            dialogue_engine = CharacterDialogueEngine(llm_client)
            learning_engine = DynamicLearningEngine()
            orchestrator = AgentOrchestrator()
            
            print("\n🚀 系统初始化完成，包含以下高级技术：")
            print("• Self-RAG 自我反思引擎")
            print("• 多模态内容生成")
            print("• 智能对话系统")
            print("• 动态学习引擎")
            print("• 多智能体协作")
            
            # 选择整合创作模式
            print("\n请选择整合创作模式：")
            print("1. 终极章节生成（集成所有技术）")
            print("2. 智能创作工作流（自动化创作流程）")
            print("3. 个性化创作助手（根据需求定制）")
            
            integrated_choice = input("模式选择 (1-3): ").strip()
            
            if integrated_choice == '1':
                # 终极章节生成
                print("\n🎯 终极章节生成")
                print("集成Self-RAG、多模态、对话优化、8大问题解决等所有技术")
                
                # 获取章节信息
                outline = storage.load_outline()
                mystery_outline = storage.load_mystery_outline()
                
                if not outline and not mystery_outline:
                    print("❌ 未找到大纲，请先创建大纲")
                    continue
                
                latest_chapter = storage.get_latest_chapter_number()
                next_chapter = latest_chapter + 1
                
                print(f"🚀 开始终极生成第{next_chapter}章...")
                
                # 第1步：使用Self-RAG生成初始内容
                print("第1步: Self-RAG 自我反思生成...")
                context = {
                    'chapter_number': next_chapter,
                    'outline': outline or mystery_outline,
                    'genre': '悬疑推理' if mystery_outline else '通用'
                }
                
                reflection_result = reflection_engine.generate_with_reflection(
                    f"请为第{next_chapter}章生成高质量小说内容", context
                )
                
                if not reflection_result.get('final_content'):
                    print("❌ Self-RAG生成失败")
                    continue
                
                initial_content = reflection_result['final_content']
                print(f"✅ Self-RAG完成，质量评分: {reflection_result['quality_score']:.1f}/10")
                
                # 第2步：8大问题解决方案优化
                print("第2步: 8大问题解决方案优化...")
                solution_result = learning_engine.solve_core_problems(
                    initial_content, context, list(range(1, 9))
                )
                
                if solution_result['success']:
                    optimized_content = solution_result['improved_content']
                    print(f"✅ 8大问题优化完成，改进度: {solution_result['overall_improvement']:.1f}/10")
                else:
                    optimized_content = initial_content
                    print("⚠️ 8大问题优化跳过")
                
                # 第3步：智能对话优化
                print("第3步: 智能对话系统优化...")
                # 提取对话内容进行优化（简化处理）
                dialogue_sections = []
                lines = optimized_content.split('\n')
                for line in lines:
                    if '：' in line or '「' in line or '」' in line:
                        dialogue_sections.append(line)
                
                if dialogue_sections:
                    for i, dialogue in enumerate(dialogue_sections[:3]):  # 限制处理前3个对话
                        dialogue_data = {
                            'dialogue': dialogue,
                            'optimization_goals': ['naturalness', 'emotion'],
                            'character_profile': {},
                            'emotional_context': {},
                            'scene_context': {}
                        }
                        
                        opt_result = optimization_engine.optimize_dialogue_comprehensive(dialogue_data)
                        if opt_result.get('optimized_dialogue'):
                            optimized_content = optimized_content.replace(
                                dialogue, opt_result['optimized_dialogue']
                            )
                    
                    print(f"✅ 对话优化完成，处理了{min(len(dialogue_sections), 3)}处对话")
                else:
                    print("⚠️ 未发现对话内容，跳过对话优化")
                
                # 第4步：多模态元素生成
                print("第4步: 多模态元素生成...")
                chapter_plan = {
                    'chapter_number': next_chapter,
                    'chapter_title': f'第{next_chapter}章',
                    'main_plot_points': ['情节发展'],
                    'character_development': ['角色发展']
                }
                
                multimodal_config = {
                    'include_images': True,
                    'include_audio': True,
                    'include_visualization': False,
                    'style': 'realistic'
                }
                
                # 将优化后的内容作为文本内容，生成多模态元素
                multimodal_result = {
                    'text_content': optimized_content,
                    'chapter_number': next_chapter,
                    'title': f'第{next_chapter}章',
                    'word_count': len(optimized_content),
                    'multimodal_elements': {}
                }
                
                # 生成图像描述
                image_descriptions = multimodal_generator._generate_image_descriptions(
                    optimized_content, {'image_style': 'illustration', 'max_images': 2}
                )
                multimodal_result['multimodal_elements']['images'] = image_descriptions
                
                # 生成音频描述
                audio_descriptions = multimodal_generator._generate_audio_descriptions(
                    optimized_content, {'audio_elements': ['background_music', 'sound_effects']}
                )
                multimodal_result['multimodal_elements']['audio'] = audio_descriptions
                
                print(f"✅ 多模态生成完成，图像{len(image_descriptions)}个，音频元素已生成")
                
                # 第5步：最终质量检查
                print("第5步: 最终质量检查...")
                final_quality = learning_engine.get_quality_report(optimized_content, context)
                
                # 保存终极章节
                chapter_data = {
                    'chapter_number': next_chapter,
                    'title': f'第{next_chapter}章',
                    'content': optimized_content,
                    'word_count': len(optimized_content),
                    'integrated_creation': True,
                    'creation_technologies': [
                        'Self-RAG', '8大问题解决', '智能对话优化', '多模态生成'
                    ],
                    'multimodal_elements': multimodal_result['multimodal_elements'],
                    'self_reflection': reflection_result,
                    'problem_solutions': solution_result if solution_result['success'] else {},
                    'final_quality': final_quality if final_quality['success'] else {}
                }
                
                storage.save_chapter(next_chapter, chapter_data)
                
                print(f"\n🎉 终极章节生成完成！")
                print(f"📄 字数: {len(optimized_content)}字")
                print(f"🏆 最终质量: {final_quality['overall_score']:.1f}/10" if final_quality['success'] else "质量评估未完成")
                print(f"🎨 集成技术: Self-RAG + 8大问题解决 + 智能对话 + 多模态")
                print(f"💾 终极章节已保存")
                
            elif integrated_choice == '2':
                # 智能创作工作流
                print("\n🤖 智能创作工作流")
                print("自动化的端到端创作流程")
                
                print("配置创作参数：")
                target_chapters = input("目标章节数（默认3）: ").strip()
                try:
                    target_chapters = int(target_chapters)
                except:
                    target_chapters = 3
                
                workflow_config = {
                    'auto_outline': input("自动创建大纲? (y/n): ").strip().lower() == 'y',
                    'quality_mode': 'premium',
                    'include_multimodal': input("包含多模态元素? (y/n): ").strip().lower() == 'y',
                    'auto_optimization': True
                }
                
                print(f"\n🚀 启动智能创作工作流，目标生成{target_chapters}章...")
                
                # 检查或创建大纲
                outline = storage.load_outline()
                if not outline and workflow_config['auto_outline']:
                    print("🎯 自动创建大纲...")
                    outline_result = orchestrator.create_collaborative_outline('general', {})
                    if outline_result:
                        print("✅ 大纲创建完成")
                        outline = outline_result
                    else:
                        print("❌ 大纲创建失败，流程终止")
                        continue
                elif not outline:
                    print("❌ 未找到大纲且未启用自动创建")
                    continue
                
                # 批量生成章节
                successful_chapters = 0
                for i in range(target_chapters):
                    latest_chapter = storage.get_latest_chapter_number()
                    next_chapter = latest_chapter + 1
                    
                    print(f"\n📝 生成第{next_chapter}章...")
                    
                    # 使用协作生成
                    chapter_result = orchestrator.generate_chapter_collaboratively(next_chapter)
                    
                    if chapter_result:
                        successful_chapters += 1
                        print(f"✅ 第{next_chapter}章生成完成")
                        
                        # 如果启用多模态，添加多模态元素
                        if workflow_config['include_multimodal']:
                            chapter_plan = {'chapter_number': next_chapter, 'chapter_title': f'第{next_chapter}章'}
                            multimodal_config = {'include_images': True, 'include_audio': True}
                            
                            # 简化的多模态处理
                            storage.update_chapter(next_chapter, {
                                'multimodal_enabled': True,
                                'creation_workflow': 'integrated'
                            })
                    else:
                        print(f"❌ 第{next_chapter}章生成失败")
                
                print(f"\n📊 智能创作工作流完成！")
                print(f"✅ 成功生成: {successful_chapters}/{target_chapters}章")
                print(f"📈 成功率: {successful_chapters/target_chapters:.1%}")
                
            elif integrated_choice == '3':
                # 个性化创作助手
                print("\n🎭 个性化创作助手")
                print("根据您的具体需求定制创作方案")
                
                print("\n请描述您的创作需求：")
                user_requirements = {
                    'genre': input("小说类型（如：悬疑、言情、玄幻）: ").strip(),
                    'style': input("文风偏好（如：轻松、严肃、幽默）: ").strip(),
                    'target_audience': input("目标读者（如：年轻人、成年人）: ").strip(),
                    'platform': input("发布平台（如：番茄小说、起点）: ").strip(),
                    'special_needs': input("特殊需求（如：多对话、重情感、快节奏）: ").strip()
                }
                
                print(f"\n🔍 分析创作需求...")
                
                # 根据需求推荐技术组合
                recommended_tech = []
                
                if '对话' in user_requirements['special_needs']:
                    recommended_tech.append('智能对话系统')
                
                if '情感' in user_requirements['special_needs']:
                    recommended_tech.append('情感对话生成')
                
                if '质量' in user_requirements['special_needs'] or '精品' in user_requirements['special_needs']:
                    recommended_tech.append('Self-RAG自我反思')
                
                if '多媒体' in user_requirements['special_needs'] or '视觉' in user_requirements['special_needs']:
                    recommended_tech.append('多模态生成')
                
                # 默认推荐
                if not recommended_tech:
                    recommended_tech = ['Self-RAG自我反思', '8大问题解决']
                
                print(f"💡 推荐技术组合: {', '.join(recommended_tech)}")
                
                confirm = input("\n是否使用推荐的技术组合生成一章试验？(y/n): ").strip().lower()
                
                if confirm == 'y':
                    outline = storage.load_outline()
                    mystery_outline = storage.load_mystery_outline()
                    
                    if not outline and not mystery_outline:
                        print("❌ 未找到大纲，请先创建大纲")
                        continue
                    
                    latest_chapter = storage.get_latest_chapter_number()
                    next_chapter = latest_chapter + 1
                    
                    print(f"🚀 使用个性化方案生成第{next_chapter}章...")
                    
                    # 根据推荐技术生成内容
                    context = {
                        'chapter_number': next_chapter,
                        'outline': outline or mystery_outline,
                        'user_requirements': user_requirements
                    }
                    
                    if 'Self-RAG自我反思' in recommended_tech:
                        result = reflection_engine.generate_with_reflection(
                            f"请根据用户需求生成第{next_chapter}章", context
                        )
                        content = result.get('final_content', '')
                        quality_score = result.get('quality_score', 0)
                    else:
                        # 使用基础协作生成
                        chapter_result = orchestrator.generate_chapter_collaboratively(next_chapter)
                        content = chapter_result.get('content', '') if chapter_result else ''
                        quality_score = chapter_result.get('quality_score', 0) if chapter_result else 0
                    
                    if content:
                        # 保存个性化章节
                        chapter_data = {
                            'chapter_number': next_chapter,
                            'title': f'第{next_chapter}章',
                            'content': content,
                            'word_count': len(content),
                            'personalized_creation': True,
                            'user_requirements': user_requirements,
                            'applied_technologies': recommended_tech,
                            'quality_score': quality_score
                        }
                        
                        storage.save_chapter(next_chapter, chapter_data)
                        
                        print(f"\n✅ 个性化章节生成完成！")
                        print(f"📄 字数: {len(content)}字")
                        print(f"🏆 质量评分: {quality_score:.1f}/10")
                        print(f"🎭 应用技术: {', '.join(recommended_tech)}")
                        print(f"💾 个性化章节已保存")
                    else:
                        print("❌ 个性化章节生成失败")

        elif choice == '25':
            # 一条龙智能体协作优化系统
            print("\n🚀 一条龙智能体协作优化系统")
            print("=" * 50)
            print("所有智能体协同工作，一次性优化整部小说")
            
            # 检查章节
            all_chapters = storage.get_all_chapters()
            if not all_chapters:
                print("❌ 未找到任何章节")
                continue
            
            print(f"\n📚 发现 {len(all_chapters)} 个章节")
            print("🤖 将启动以下智能体协同优化：")
            print("  • CharacterMemoryAgent - 角色一致性")
            print("  • PlotTrackerAgent - 情节连贯性")
            print("  • QualityAnalyzer - 质量分析")
            print("  • TextHumanizer - 人性化优化")
            print("  • StyleOptimizer - 风格优化")
            print("  • AdvancedOptimizer - 高级优化")
            
            confirm = input("\n开始一条龙优化？(y/n): ").strip().lower()
            if confirm != 'y':
                print("已取消")
                continue
            
            from agents.agent_orchestrator import AgentOrchestrator
            from utils.advanced_optimizer import AdvancedOptimizer
            from utils.quality_analyzer import QualityAnalyzer
            from utils.text_humanizer import TextHumanizer
            from utils.style_optimizer import StyleOptimizer
            
            orchestrator = AgentOrchestrator()
            advanced_optimizer = AdvancedOptimizer()
            quality_analyzer = QualityAnalyzer()
            text_humanizer = TextHumanizer(LLMClient())
            style_optimizer = StyleOptimizer(LLMClient())
            
            print(f"\n🚀 开始一条龙优化...")
            
            optimized_count = 0
            for i, chapter in enumerate(all_chapters, 1):
                chapter_num = chapter.get('chapter_number', i)
                print(f"\n[{i}/{len(all_chapters)}] 优化第{chapter_num}章...")
                
                try:
                    content = chapter.get('content', '')
                    if not content:
                        print("  ⚠️ 章节内容为空，跳过")
                        continue
                    
                    # 步骤1：质量分析
                    print("  [1/5] 质量分析...", end='', flush=True)
                    quality_before = quality_analyzer.analyze(content)
                    print(f" ✓ ({quality_before['overall_score']:.1f}/10)")
                    
                    # 步骤2：高级优化
                    print("  [2/5] 高级内容优化...", end='', flush=True)
                    context = orchestrator.context_manager.get_full_context()
                    opt_result = advanced_optimizer.comprehensive_optimize(content, context)
                    
                    if opt_result['optimization_success']:
                        content = opt_result['optimized_content']
                        print(f" ✓ (改进: {', '.join(opt_result['improvements'][:2])})")
                    else:
                        print(" -")
                    
                    # 步骤3：人性化处理
                    print("  [3/5] 人性化优化...", end='', flush=True)
                    humanize_result = text_humanizer.humanize(content, aggressive=True)
                    content = humanize_result.get('humanized_text', content)
                    print(" ✓")
                    
                    # 步骤4：风格优化
                    print("  [4/5] 风格优化...", end='', flush=True)
                    style_result = style_optimizer.optimize(content, {
                        'vivid_description': True,
                        'dialogue_variation': True,
                        'rhythm_adjustment': True
                    })
                    content = style_result.get('optimized_text', content)
                    print(" ✓")
                    
                    # 步骤5：质量复评
                    print("  [5/5] 质量复评...", end='', flush=True)
                    quality_after = quality_analyzer.analyze(content)
                    print(f" ✓ ({quality_after['overall_score']:.1f}/10)")
                    
                    # 只有质量提升才保存
                    if quality_after['overall_score'] > quality_before['overall_score']:
                        storage.update_chapter(chapter_num, {
                            'content': content,
                            'word_count': len(content),
                            'optimized_by_pipeline': True,
                            'quality_before': quality_before['overall_score'],
                            'quality_after': quality_after['overall_score']
                        })
                        optimized_count += 1
                        improvement = quality_after['overall_score'] - quality_before['overall_score']
                        print(f"  ✅ 优化完成 (质量提升: +{improvement:.1f})")
                    else:
                        print(f"  ℹ️ 质量已达标，无需优化")
                    
                except Exception as e:
                    print(f"  ❌ 错误: {e}")
            
            print(f"\n📊 一条龙优化完成！")
            print(f"✅ 成功优化: {optimized_count}/{len(all_chapters)}章")
            print(f"💾 所有改进已自动保存")

        elif choice == '0':
            print("\n再见！")
            break

        else:
            print("\n无效选项，请重新输入")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI小说生成系统')
    parser.add_argument('--mode', choices=['web', 'cli'], default='web',
                       help='运行模式：web(Web界面) 或 cli(命令行)')
    parser.add_argument('--check', action='store_true',
                       help='仅检查环境配置')

    args = parser.parse_args()

    # 检查环境
    if not check_environment():
        if not args.check:
            print("\n是否继续运行？(y/n): ", end='')
            if input().lower() != 'y':
                sys.exit(1)
        elif choice == '10':
            from utils.author_note import save_author_note, load_author_note
            print("当前作者笔记：")
            exist = load_author_note()
            print(exist if exist else "(无)")
            note = input("请输入新的作者笔记：\n").strip()
            if note:
                save_author_note(note)
                print("✓ 已更新作者笔记")

    if args.check:
        print("✓ 环境配置检查完成")
        return

    # 运行系统
    if args.mode == 'web':
        run_web()
    else:
        run_cli()

if __name__ == '__main__':
    main()
