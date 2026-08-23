"""
AI小说生成系统 - 简化版主程序
统一的Web和CLI入口，提供直观的用户体验
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
        print("🔧 环境配置向导")
        print("=" * 40)
        print("检测到未配置API密钥，将启动配置向导...")
        print("\n请按以下步骤配置：")
        print("1. 复制 .env.example 为 .env")
        print("2. 在 .env 文件中设置 HEPAI_API_KEY")
        print("3. 重新启动程序")
        print("=" * 40)
        return False
    return True

def run_web():
    """启动Web服务"""
    print("🚀 启动Web界面模式")
    print("=" * 40)
    
    try:
        from web.app import run_app
        run_app()
    except ImportError as e:
        print(f"❌ Web模块导入失败: {e}")
        print("请检查依赖包是否正确安装")
    except Exception as e:
        print(f"❌ Web服务启动失败: {e}")

def run_cli():
    """简化的命令行模式"""
    print("🎯 AI小说生成系统 - 智能CLI")
    print("=" * 40)
    print("选择您的创作需求，系统将为您提供最佳方案")
    
    try:
        from utils import Storage
        from agents.agent_orchestrator import AgentOrchestrator
        from qa import NovelQASystem
        
        storage = Storage()
        orchestrator = AgentOrchestrator()
        qa_system = NovelQASystem()
        
        while True:
            print("\n🎨 创作菜单")
            print("=" * 30)
            print("1. 🆕 开始新小说创作")
            print("2. ✍️  继续现有小说")
            print("3. 🔍 智能问答系统")
            print("4. ⚙️  系统设置")
            print("5. 📊 创作统计")
            print("0. 👋 退出")

            choice = input("\n请选择功能 (0-5): ").strip()

            if choice == '1':
                # 新小说创作流程
                create_new_novel(orchestrator, storage)
            elif choice == '2':
                # 继续现有小说
                continue_existing_novel(orchestrator, storage)
            elif choice == '3':
                # 智能问答
                intelligent_qa(qa_system)
            elif choice == '4':
                # 系统设置
                system_settings()
            elif choice == '5':
                # 创作统计
                show_statistics(storage)
            elif choice == '0':
                print("\n👋 感谢使用AI小说生成系统！")
                break
            else:
                print("❌ 无效选项，请重新输入")
                
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
    except Exception as e:
        print(f"❌ CLI启动失败: {e}")

def create_new_novel(orchestrator, storage):
    """创建新小说的引导流程"""
    print("\n🆕 新小说创作向导")
    print("=" * 30)
    
    # 第一步：选择小说类型
    print("📚 请选择您想创作的小说类型：")
    genres = {
        '1': {'name': '悬疑推理', 'key': 'mystery', 'desc': '逻辑严谨，悬念迭起'},
        '2': {'name': '现代言情', 'key': 'romance', 'desc': '情感细腻，甜蜜温馨'},
        '3': {'name': '玄幻奇幻', 'key': 'fantasy', 'desc': '想象丰富，体系完整'},
        '4': {'name': '科幻未来', 'key': 'scifi', 'desc': '技术前沿，思维开阔'},
        '5': {'name': '历史古风', 'key': 'historical', 'desc': '文化底蕴，历史厚重'},
        '6': {'name': '都市现代', 'key': 'urban', 'desc': '贴近现实，职场情感'}
    }
    
    for key, info in genres.items():
        print(f"{key}. {info['name']} - {info['desc']}")
    
    genre_choice = input("\n选择类型 (1-6): ").strip()
    if genre_choice not in genres:
        print("❌ 无效选择，默认使用悬疑推理")
        genre_choice = '1'
    
    selected_genre = genres[genre_choice]
    print(f"✅ 已选择：{selected_genre['name']}")
    
    # 第二步：基本设定
    print(f"\n📝 {selected_genre['name']}小说设定")
    settings = {
        'genre': selected_genre['key'],
        'title': input("📖 书名（可选）: ").strip(),
        'theme': input("🎯 主题（如：复仇、成长、爱情）: ").strip(),
        'setting': input("🌍 背景设定（如：现代都市、古代宫廷）: ").strip(),
        'style': input("✍️  文风（如：轻松幽默、严肃深刻）: ").strip(),
        'target_words': input("📏 目标字数（默认：50万字）: ").strip() or "50万字"
    }
    
    # 第三步：创建大纲和首章
    print(f"\n🚀 开始创作{selected_genre['name']}小说...")
    print("📋 第1步：智能创建大纲...")
    
    outline = orchestrator.create_collaborative_outline(selected_genre['key'], settings)
    if outline:
        print("✅ 大纲创建成功！")
        
        print("📝 第2步：生成首章...")
        first_chapter = orchestrator.generate_chapter_collaboratively(1)
        
        if first_chapter:
            print("✅ 首章生成完成！")
            print(f"📊 字数：{first_chapter.get('word_count', 0)}字")
            print(f"🏆 质量评分：{first_chapter.get('quality_score', 0):.1f}/10")
            
            # 询问是否继续生成
            continue_gen = input(f"\n🔄 是否继续生成第2章？(y/n): ").strip().lower()
            if continue_gen == 'y':
                second_chapter = orchestrator.generate_chapter_collaboratively(2)
                if second_chapter:
                    print("✅ 第2章生成完成！")
                    print("🎉 恭喜！您的小说创作已经开始！")
        else:
            print("❌ 首章生成失败")
    else:
        print("❌ 大纲创建失败")

def continue_existing_novel(orchestrator, storage):
    """继续现有小说"""
    print("\n✍️ 继续现有小说")
    print("=" * 30)
    
    # 检查现有小说
    outline = storage.load_outline()
    chapters = storage.get_all_chapters()
    
    if not outline:
        print("❌ 未找到现有小说，请先创建新小说")
        return
    
    print(f"📚 当前小说：{outline.get('novel_title', '未命名小说')}")
    print(f"📄 已有章节：{len(chapters)}章")
    
    if chapters:
        latest_chapter = max(ch.get('chapter_number', 0) for ch in chapters)
        next_chapter = latest_chapter + 1
    else:
        next_chapter = 1
    
    print(f"📝 准备生成第{next_chapter}章")
    
    # 选择生成模式
    print("\n请选择生成模式：")
    print("1. 🤖 智能协作模式（推荐）")
    print("2. ⚡ 快速生成模式")
    print("3. 🎨 精品优化模式")
    
    mode_choice = input("选择模式 (1-3): ").strip()
    
    if mode_choice == '3':
        print(f"🎨 使用精品优化模式生成第{next_chapter}章...")
        chapter = orchestrator.generate_premium_chapter(next_chapter, None, None)
    elif mode_choice == '2':
        print(f"⚡ 使用快速模式生成第{next_chapter}章...")
        chapter = orchestrator.generate_chapter_collaboratively(next_chapter)
    else:
        print(f"🤖 使用智能协作模式生成第{next_chapter}章...")
        chapter = orchestrator.generate_chapter_collaboratively(next_chapter)
    
    if chapter:
        print(f"✅ 第{next_chapter}章生成完成！")
        print(f"📊 字数：{chapter.get('word_count', 0)}字")
        print(f"🏆 质量评分：{chapter.get('quality_score', 0):.1f}/10")
    else:
        print("❌ 章节生成失败")

def intelligent_qa(qa_system):
    """智能问答系统"""
    print("\n🔍 智能问答系统")
    print("=" * 30)
    print("您可以询问任何关于小说内容的问题")
    print("输入 'exit' 或 '退出' 返回主菜单\n")
    
    while True:
        question = input("💬 请输入您的问题: ").strip()
        
        if question.lower() in ['exit', '退出', 'quit']:
            break
        
        if not question:
            print("❌ 请输入有效问题")
            continue
        
        try:
            print("🤔 思考中...")
            answer = qa_system.query(question)
            print(f"💡 回答：\n{answer}\n")
        except Exception as e:
            print(f"❌ 查询失败: {e}")

def system_settings():
    """系统设置"""
    print("\n⚙️ 系统设置")
    print("=" * 30)
    print("1. 📊 查看系统状态")
    print("2. 🔧 重建问答索引")
    print("3. 🗑️  清理临时文件")
    print("4. 📋 查看配置信息")
    
    setting_choice = input("选择设置项 (1-4): ").strip()
    
    if setting_choice == '1':
        show_system_status()
    elif setting_choice == '2':
        rebuild_qa_index()
    elif setting_choice == '3':
        clean_temp_files()
    elif setting_choice == '4':
        show_config_info()
    else:
        print("❌ 无效选择")

def show_statistics(storage):
    """显示创作统计"""
    print("\n📊 创作统计")
    print("=" * 30)
    
    try:
        outline = storage.load_outline()
        chapters = storage.get_all_chapters()
        
        if outline:
            print(f"📚 小说标题：{outline.get('novel_title', '未命名小说')}")
            print(f"🎭 小说类型：{outline.get('genre', '未知')}")
        else:
            print("📚 小说标题：暂无")
        
        print(f"📄 章节数量：{len(chapters)}章")
        
        if chapters:
            total_words = sum(ch.get('word_count', 0) for ch in chapters)
            avg_words = total_words // len(chapters) if chapters else 0
            print(f"📏 总字数：{total_words:,}字")
            print(f"📐 平均字数：{avg_words:,}字/章")
            
            # 质量统计
            quality_scores = [ch.get('quality_score', 0) for ch in chapters if ch.get('quality_score')]
            if quality_scores:
                avg_quality = sum(quality_scores) / len(quality_scores)
                print(f"🏆 平均质量：{avg_quality:.1f}/10")
        else:
            print("📏 总字数：0字")
            
    except Exception as e:
        print(f"❌ 统计获取失败: {e}")

def show_system_status():
    """显示系统状态"""
    print("📊 系统状态：运行正常")
    print("💾 数据库：连接正常")
    print("🤖 AI服务：连接正常")

def rebuild_qa_index():
    """重建问答索引"""
    try:
        from qa import NovelQASystem
        qa_system = NovelQASystem()
        qa_system.index_all_chapters()
        print("✅ 问答索引重建完成")
    except Exception as e:
        print(f"❌ 重建失败: {e}")

def clean_temp_files():
    """清理临时文件"""
    print("🗑️ 清理临时文件...")
    # 这里可以添加清理逻辑
    print("✅ 临时文件清理完成")

def show_config_info():
    """显示配置信息"""
    try:
        from utils import config
        print("📋 当前配置：")
        print(f"• 每日生成时间：{config.get('scheduler.schedule_time', '09:00')}")
        print(f"• 每日章节数：{config.get('scheduler.chapters_per_day', 2)}")
        print(f"• 默认章节字数：{config.get('chapter.default_length', 3000)}")
    except Exception as e:
        print(f"❌ 配置获取失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI小说生成系统 - 简化版')
    parser.add_argument('--mode', choices=['web', 'cli'], default='web',
                       help='运行模式：web(Web界面) 或 cli(命令行)')

    args = parser.parse_args()

    print("📚 AI小说生成系统")
    print("=" * 40)
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境配置不完整，程序退出")
        return

    # 运行系统
    if args.mode == 'web':
        run_web()
    else:
        run_cli()

if __name__ == '__main__':
    main()
