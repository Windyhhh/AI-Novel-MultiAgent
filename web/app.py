"""Web应用主程序 - 增强版"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from agents import OutlineAgent, ChapterPlanningAgent, ContentGenerationAgent
from agents.agent_factory import AgentFactory, GenreAgentRegistry
from scheduler import NovelScheduler
from qa import NovelQASystem
from integrations import FeedbackProcessor
from utils import Storage, config, get_logger, perf_logger, system_monitor

# 配置日志
logger = get_logger('web_app')

app = Flask(__name__)
CORS(app)

# 初始化组件
storage = Storage()
outline_agent = OutlineAgent()
planning_agent = ChapterPlanningAgent()
generation_agent = ContentGenerationAgent()
scheduler = NovelScheduler()
qa_system = NovelQASystem()
feedback_processor = FeedbackProcessor()

# 初始化智能体工厂
agent_factory = AgentFactory()
genre_registry = GenreAgentRegistry()

# ==================== 页面路由 ====================

@app.route('/')
def index():
    """首页 - 使用新的现代化界面"""
    return render_template('index_new.html')

@app.route('/old')
def old_index():
    """旧版界面"""
    return render_template('index.html')

@app.route('/chapters')
def chapters_page():
    """章节列表页面"""
    return render_template('chapters.html')

@app.route('/qa')
def qa_page():
    """问答页面"""
    return render_template('qa.html')

@app.route('/settings')
def settings_page():
    """设置页面"""
    return render_template('settings.html')

@app.route('/advanced')
def advanced_page():
    """高级功能页面"""
    return render_template('advanced.html')

@app.route('/agents')
def agents_page():
    """智能体选择页面"""
    return render_template('agents.html')

@app.route('/novel')
def novel_viewer():
    """小说查看器页面"""
    return render_template('novel_viewer.html')

@app.route('/optimize')
def optimize_page():
    """一条龙优化系统页面"""
    return render_template('optimize.html')

# ==================== API路由 ====================

@app.route('/api/outline', methods=['GET'])
def get_outline():
    """获取大纲"""
    outline = storage.load_outline()
    if outline:
        return jsonify({'success': True, 'data': outline})
    else:
        return jsonify({'success': False, 'message': '未找到大纲'})

# ==================== 智能体选择API ====================

@app.route('/api/agents/list', methods=['GET'])
def list_agents():
    """获取所有可用的智能体类型"""
    try:
        agents_info = agent_factory.list_available_agents()
        
        # 添加详细的智能体信息
        detailed_agents = {
            'romance': {
                'name': '言情小说',
                'description': '专注于情感发展和浪漫情节的小说创作',
                'keywords': ['言情', '恋爱', '浪漫', '情感'],
                'features': ['情感描写', '心理活动', '对话互动', '细节刻画'],
                'icon': '💕',
                'color': '#ff6b9d'
            },
            'fantasy': {
                'name': '玄幻小说',
                'description': '包含修炼体系和异世界观的玄幻小说创作',
                'keywords': ['玄幻', '修仙', '异界', '修炼'],
                'features': ['世界观构建', '力量体系', '战斗描写', '升级爽感'],
                'icon': '⚔️',
                'color': '#9c88ff'
            },
            'scifi': {
                'name': '科幻小说',
                'description': '基于科学理论的未来世界小说创作',
                'keywords': ['科幻', '未来', '科技', '星际'],
                'features': ['科技描写', '逻辑严谨', '想象力', '社会思考'],
                'icon': '🚀',
                'color': '#4dabf7'
            },
            'historical': {
                'name': '历史小说',
                'description': '基于真实历史背景的小说创作',
                'keywords': ['历史', '古代', '传记', '朝代'],
                'features': ['历史考证', '人物刻画', '时代特色', '文化底蕴'],
                'icon': '🏛️',
                'color': '#fab005'
            },
            'urban': {
                'name': '都市小说',
                'description': '现代都市生活背景的现实题材小说',
                'keywords': ['都市', '现代', '职场', '商战'],
                'features': ['现实感', '职场描写', '情感戏份', '社会现象'],
                'icon': '🏙️',
                'color': '#51cf66'
            },
            'mystery': {
                'name': '悬疑推理',
                'description': '注重逻辑推理和悬疑氛围的小说创作',
                'keywords': ['悬疑', '推理', '犯罪', '侦探'],
                'features': ['逻辑推理', '悬疑氛围', '线索布置', '真相揭示'],
                'icon': '🔍',
                'color': '#495057'
            }
        }
        
        return jsonify({
            'success': True, 
            'data': {
                'available_agents': agents_info,
                'detailed_info': detailed_agents
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/agents/<agent_type>/outline', methods=['POST'])
def create_genre_outline(agent_type):
    """使用指定类型的智能体创建大纲"""
    data = request.json
    custom_settings = data.get('custom_settings', {})
    
    try:
        # 获取对应的智能体
        agent = agent_factory.get_agent_by_genre(agent_type)
        if not agent:
            return jsonify({'success': False, 'message': f'未找到{agent_type}类型的智能体'})
        
        # 创建大纲
        outline = agent.create_outline(custom_settings)
        
        if outline:
            # 保存大纲
            storage.save_outline(outline)
            return jsonify({'success': True, 'data': outline})
        else:
            return jsonify({'success': False, 'message': '大纲创建失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/agents/<agent_type>/chapter', methods=['POST'])
def generate_genre_chapter(agent_type):
    """使用指定类型的智能体生成章节"""
    data = request.json
    chapter_plan = data.get('chapter_plan', {})
    context = data.get('context', {})
    
    try:
        # 获取对应的智能体
        agent = agent_factory.get_agent_by_genre(agent_type)
        if not agent:
            return jsonify({'success': False, 'message': f'未找到{agent_type}类型的智能体'})
        
        # 生成章节
        chapter = agent.generate_chapter(chapter_plan, context)
        
        if chapter:
            # 保存章节
            chapter_number = chapter.get('chapter_number', 1)
            storage.save_chapter(chapter_number, chapter)
            return jsonify({'success': True, 'data': chapter})
        else:
            return jsonify({'success': False, 'message': '章节生成失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/agents/collaborative', methods=['POST'])
def create_collaborative_workflow():
    """创建协作智能体工作流"""
    data = request.json
    genre = data.get('genre', '')
    platform = data.get('platform', 'tomato_novel')
    custom_settings = data.get('custom_settings', {})
    
    try:
        # 创建协作智能体组合
        agents = agent_factory.create_collaborative_agents(genre, platform)
        
        workflow_result = {}
        
        # 1. 使用大纲智能体创建大纲
        if 'outline' in agents and agents['outline']:
            outline = agents['outline'].create_outline('autonomous', custom_settings)
            if outline:
                workflow_result['outline'] = outline
                storage.save_outline(outline)
        
        # 2. 使用章节规划智能体规划章节 (简化版本)
        if 'chapter_planning' in agents and workflow_result.get('outline'):
            # 创建简单的章节规划
            chapter_plans = []
            for i in range(1, 4):  # 生成前3章的规划
                chapter_plan = {
                    'chapter_number': i,
                    'title': f'第{i}章',
                    'main_content': f'根据大纲进行第{i}章的内容创作',
                    'character_focus': '主要角色发展',
                    'plot_advancement': f'推进主要情节线'
                }
                chapter_plans.append(chapter_plan)
            workflow_result['chapter_plans'] = chapter_plans
        
        # 3. 使用类型专用智能体生成第一章
        genre_agent = None
        if genre.lower() in ['言情', 'romance'] and 'romance' in agents:
            genre_agent = agents['romance']
        elif genre.lower() in ['玄幻', 'fantasy'] and 'fantasy' in agents:
            genre_agent = agents['fantasy']
        elif genre.lower() in ['科幻', 'scifi'] and 'scifi' in agents:
            genre_agent = agents['scifi']
        elif genre.lower() in ['历史', 'historical'] and 'historical' in agents:
            genre_agent = agents['historical']
        elif genre.lower() in ['都市', 'urban'] and 'urban' in agents:
            genre_agent = agents['urban']
        elif genre.lower() in ['悬疑', 'mystery'] and 'mystery' in agents:
            genre_agent = agents['mystery']
        
        # 如果没有找到专用智能体，使用通用内容生成智能体
        if not genre_agent and 'content_generation' in agents:
            genre_agent = agents['content_generation']
        
        # 生成第一章
        if genre_agent and workflow_result.get('chapter_plans'):
            first_chapter_plan = workflow_result['chapter_plans'][0]
            context = {
                'outline': workflow_result.get('outline', {}),
                'genre': genre,
                'platform': platform,
                'custom_settings': custom_settings
            }
            first_chapter = genre_agent.generate_chapter(first_chapter_plan, context)
            if first_chapter:
                workflow_result['first_chapter'] = first_chapter
                storage.save_chapter(1, first_chapter)
        
        return jsonify({
            'success': True, 
            'data': {
                'workflow_result': workflow_result,
                'agents_used': list(agents.keys()),
                'genre': genre,
                'platform': platform,
                'generated_content': {
                    'outline_created': bool(workflow_result.get('outline')),
                    'chapter_plans_created': bool(workflow_result.get('chapter_plans')),
                    'first_chapter_generated': bool(workflow_result.get('first_chapter'))
                }
            }
        })
    except Exception as e:
        logger.error(f"协作工作流执行失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/genres/recommendations', methods=['POST'])
def get_genre_recommendations():
    """根据用户需求推荐合适的智能体类型"""
    data = request.json
    requirements = data.get('requirements', {})
    
    try:
        suitable_agents = genre_registry.get_suitable_agents(requirements)
        
        # 获取推荐理由
        recommendations = []
        for agent_type in suitable_agents[:3]:  # 推荐前3个
            if agent_type in ['romance', 'fantasy', 'scifi', 'historical', 'urban', 'mystery']:
                agent_info = {
                    'type': agent_type,
                    'confidence': 0.8,  # 可以基于匹配度计算
                    'reason': f"基于您的需求，{agent_type}智能体最适合"
                }
                recommendations.append(agent_info)
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': recommendations,
                'all_suitable': suitable_agents
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# ==================== 新增高级功能API ====================

@app.route('/api/intelligent_recommend', methods=['POST'])
def intelligent_recommend():
    """智能推荐功能"""
    from utils.intelligent_recommendation import IntelligentRecommendationEngine
    
    data = request.json
    user_input = data.get('user_input', {})
    
    try:
        engine = IntelligentRecommendationEngine()
        user_needs = engine.analyze_user_needs(user_input)
        recommendations = engine.generate_recommendations(user_needs)
        
        return jsonify({'success': True, 'data': recommendations})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/workflow_execute', methods=['POST'])
def workflow_execute():
    """执行推荐工作流"""
    from utils.intelligent_recommendation import WorkflowExecutor
    
    data = request.json
    workflow = data.get('workflow', {})
    config = data.get('config', {})
    
    try:
        executor = WorkflowExecutor()
        result = executor.execute_workflow(workflow, config)
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/self_rag/generate', methods=['POST'])
def self_rag_generate():
    """Self-RAG内容生成"""
    from utils.self_reflection_engine import SelfReflectionEngine
    from utils import LLMClient
    
    data = request.json
    prompt = data.get('prompt', '')
    context = data.get('context', {})
    
    try:
        engine = SelfReflectionEngine(LLMClient())
        result = engine.generate_with_reflection(prompt, context)
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/multimodal/generate', methods=['POST'])
def multimodal_generate():
    """多模态内容生成"""
    from utils.multimodal_generator import MultimodalGenerator
    from utils import LLMClient
    
    data = request.json
    chapter_plan = data.get('chapter_plan', {})
    config = data.get('config', {})
    
    try:
        generator = MultimodalGenerator(LLMClient())
        result = generator.generate_multimodal_chapter(chapter_plan, config)
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/dialogue/generate', methods=['POST'])
def dialogue_generate():
    """智能对话生成"""
    from utils.intelligent_dialogue_system import CharacterDialogueEngine
    from utils import LLMClient
    
    data = request.json
    character_name = data.get('character_name', '')
    context = data.get('context', {})
    target_character = data.get('target_character')
    
    try:
        engine = CharacterDialogueEngine(LLMClient())
        result = engine.generate_character_dialogue(character_name, context, target_character)
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/dialogue/optimize', methods=['POST'])
def dialogue_optimize():
    """对话优化"""
    from utils.intelligent_dialogue_system import DialogueOptimizationEngine
    from utils import LLMClient
    
    data = request.json
    dialogue_data = data.get('dialogue_data', {})
    
    try:
        engine = DialogueOptimizationEngine(LLMClient())
        result = engine.optimize_dialogue_comprehensive(dialogue_data)
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/learning/analyze', methods=['POST'])
def learning_analyze():
    """爆款小说学习分析"""
    from utils.dynamic_learning_engine import DynamicLearningEngine
    
    data = request.json
    genre = data.get('genre', '')
    sample_texts = data.get('sample_texts', [])
    
    try:
        engine = DynamicLearningEngine()
        result = engine.analyze_bestseller_patterns(genre, sample_texts)
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/quality/analyze', methods=['POST'])
def quality_analyze():
    """内容质量分析"""
    from utils.dynamic_learning_engine import DynamicLearningEngine
    
    data = request.json
    content = data.get('content', '')
    context = data.get('context', {})
    
    try:
        engine = DynamicLearningEngine()
        result = engine.get_quality_report(content, context)
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/advanced/solve_problems', methods=['POST'])
def solve_problems():
    """8大问题解决方案"""
    from utils.dynamic_learning_engine import DynamicLearningEngine
    
    data = request.json
    content = data.get('content', '')
    context = data.get('context', {})
    problems = data.get('problems', list(range(1, 9)))
    
    try:
        engine = DynamicLearningEngine()
        result = engine.solve_core_problems(content, context, problems)
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/outline', methods=['POST'])
def create_outline():
    """创建大纲"""
    data = request.json
    mode = data.get('mode', 'autonomous')
    custom_settings = data.get('custom_settings')
    
    try:
        outline = outline_agent.create_outline(mode=mode, custom_settings=custom_settings)
        if outline:
            return jsonify({'success': True, 'data': outline})
        else:
            return jsonify({'success': False, 'message': '大纲创建失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/chapters', methods=['GET'])
def get_chapters():
    """获取所有章节"""
    chapters = storage.get_all_chapters()
    return jsonify({'success': True, 'data': chapters})

@app.route('/api/chapters/<int:chapter_number>', methods=['GET'])
def get_chapter(chapter_number):
    """获取指定章节"""
    chapter = storage.load_chapter(chapter_number)
    if chapter:
        return jsonify({'success': True, 'data': chapter})
    else:
        return jsonify({'success': False, 'message': f'未找到第{chapter_number}章'})

@app.route('/api/chapters/generate', methods=['POST'])
def generate_chapter():
    """生成单个章节"""
    try:
        chapter_data = scheduler.generate_single_chapter()
        if chapter_data:
            return jsonify({'success': True, 'data': chapter_data})
        else:
            return jsonify({'success': False, 'message': '章节生成失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/chapters/<int:chapter_number>/optimize', methods=['POST'])
def optimize_chapter(chapter_number):
    """优化章节"""
    data = request.json
    feedback = data.get('feedback', '')
    
    if not feedback:
        return jsonify({'success': False, 'message': '请提供反馈意见'})
    
    try:
        result = generation_agent.optimize_chapter(chapter_number, feedback)
        if result:
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'message': '优化失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/chapters/<int:chapter_number>/edit', methods=['POST'])
def edit_chapter(chapter_number):
    """编辑章节"""
    data = request.json
    new_title = data.get('title', '')
    new_content = data.get('content', '')
    
    if not new_content.strip():
        return jsonify({'success': False, 'message': '章节内容不能为空'})
    
    try:
        # 加载现有章节
        chapter = storage.load_chapter(chapter_number)
        if not chapter:
            return jsonify({'success': False, 'message': f'未找到第{chapter_number}章'})
        
        # 更新章节数据
        chapter['title'] = new_title
        chapter['content'] = new_content
        chapter['word_count'] = len(new_content.replace('\n', '').replace(' ', ''))
        
        # 保存更新后的章节
        storage.save_chapter(chapter_number, chapter)
        
        return jsonify({'success': True, 'data': chapter})
    except Exception as e:
        logger.error(f"编辑章节失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/chapters/<int:chapter_number>/regenerate', methods=['POST'])
def regenerate_chapter(chapter_number):
    """重新生成章节"""
    try:
        # 加载大纲和现有章节信息
        outline = storage.load_outline()
        if not outline:
            return jsonify({'success': False, 'message': '未找到小说大纲'})
        
        # 加载之前的章节作为上下文
        previous_chapters = []
        for i in range(1, chapter_number):
            prev_chapter = storage.load_chapter(i)
            if prev_chapter:
                previous_chapters.append(prev_chapter)
        
        # 构建章节规划
        chapter_plan = {
            'chapter_number': chapter_number,
            'title': f'第{chapter_number}章',
            'main_content': f'根据大纲继续第{chapter_number}章的故事发展',
            'character_focus': '继续角色发展',
            'plot_advancement': '推进主要情节线'
        }
        
        # 构建生成上下文
        context = {
            'outline': outline,
            'previous_chapters': previous_chapters,
            'chapter_plan': chapter_plan
        }
        
        # 重新生成章节
        new_chapter = generation_agent.generate_chapter(chapter_plan, context)
        
        if new_chapter:
            # 确保章节号正确
            new_chapter['chapter_number'] = chapter_number
            
            # 保存重新生成的章节
            storage.save_chapter(chapter_number, new_chapter)
            
            return jsonify({'success': True, 'data': new_chapter})
        else:
            return jsonify({'success': False, 'message': '重新生成失败'})
            
    except Exception as e:
        logger.error(f"重新生成章节失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/qa/query', methods=['POST'])
def qa_query():
    """问答查询"""
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'success': False, 'message': '请输入问题'})
    
    try:
        answer = qa_system.query(question)
        return jsonify({'success': True, 'answer': answer})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/qa/index', methods=['POST'])
def qa_index():
    """重建问答索引"""
    try:
        qa_system.index_all_chapters()
        return jsonify({'success': True, 'message': '索引重建完成'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/qa/search', methods=['POST'])
def search_chapters():
    """搜索章节"""
    data = request.json
    keyword = data.get('keyword', '')
    
    if not keyword:
        return jsonify({'success': False, 'message': '请输入关键词'})
    
    try:
        results = qa_system.search_chapters(keyword)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/scheduler/status', methods=['GET'])
def scheduler_status():
    """获取调度器状态"""
    return jsonify({
        'success': True,
        'data': {
            'enabled': config.get('scheduler.enabled', True),
            'schedule_time': config.get('scheduler.schedule_time', '09:00'),
            'chapters_per_day': config.get('scheduler.chapters_per_day', 2),
            'running': scheduler.scheduler.running if scheduler.scheduler else False
        }
    })

@app.route('/api/scheduler/update', methods=['POST'])
def update_scheduler():
    """更新调度器设置"""
    data = request.json
    schedule_time = data.get('schedule_time')
    chapters_per_day = data.get('chapters_per_day')
    
    try:
        scheduler.update_schedule(schedule_time=schedule_time, chapters_per_day=chapters_per_day)
        return jsonify({'success': True, 'message': '设置已更新'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/scheduler/trigger', methods=['POST'])
def trigger_scheduler():
    """手动触发生成任务"""
    try:
        # 在后台线程中执行
        import threading
        thread = threading.Thread(target=scheduler.manual_trigger)
        thread.start()
        return jsonify({'success': True, 'message': '生成任务已启动'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/feedback/process', methods=['POST'])
def process_feedback():
    """处理飞书反馈"""
    try:
        # 在后台线程中执行
        import threading
        thread = threading.Thread(target=feedback_processor.process_feedbacks)
        thread.start()
        return jsonify({'success': True, 'message': '反馈处理已启动'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取配置"""
    return jsonify({
        'success': True,
        'data': {
            'scheduler': {
                'enabled': config.get('scheduler.enabled', True),
                'schedule_time': config.get('scheduler.schedule_time', '09:00'),
                'chapters_per_day': config.get('scheduler.chapters_per_day', 2)
            },
            'chapter': {
                'default_length': config.get('chapter.default_length', 3000),
                'min_length': config.get('chapter.min_length', 2000),
                'max_length': config.get('chapter.max_length', 5000)
            },
            'creation_mode': {
                'mode': config.get('creation_mode.mode', 'autonomous')
            }
        }
    })

@app.route('/api/config', methods=['POST'])
def update_config():
    """更新配置"""
    data = request.json

    try:
        for key, value in data.items():
            config.set(key, value)
        config.save()
        logger.info(f"配置已更新: {list(data.keys())}")
        return jsonify({'success': True, 'message': '配置已更新'})
    except Exception as e:
        logger.error(f"更新配置失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

# ==================== 性能监控API ====================

@app.route('/api/monitor/system', methods=['GET'])
def get_system_metrics():
    """获取系统指标"""
    try:
        metrics = system_monitor.get_current_metrics()
        return jsonify({'success': True, 'data': metrics})
    except Exception as e:
        logger.error(f"获取系统指标失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/monitor/history', methods=['GET'])
def get_metrics_history():
    """获取历史指标"""
    try:
        count = request.args.get('count', 10, type=int)
        history = system_monitor.get_metrics_history(count)
        return jsonify({'success': True, 'data': history})
    except Exception as e:
        logger.error(f"获取历史指标失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/monitor/summary', methods=['GET'])
def get_monitor_summary():
    """获取监控摘要"""
    try:
        summary = system_monitor.get_summary()
        return jsonify({'success': True, 'data': summary})
    except Exception as e:
        logger.error(f"获取监控摘要失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/performance/stats', methods=['GET'])
def get_performance_stats():
    """获取性能统计"""
    try:
        # 获取各组件的统计信息
        stats = {
            'llm': generation_agent.llm.get_stats() if hasattr(generation_agent.llm, 'get_stats') else {},
            'scheduler': scheduler.get_stats() if hasattr(scheduler, 'get_stats') else {},
            'qa': qa_system.get_stats() if hasattr(qa_system, 'get_stats') else {},
            'performance': perf_logger.get_metrics()
        }
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        logger.error(f"获取性能统计失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

# ==================== 一条龙优化系统API ====================

@app.route('/api/optimize/pipeline', methods=['POST'])
def optimize_pipeline():
    """一条龙智能体协作优化系统"""
    from agents.agent_orchestrator import AgentOrchestrator
    from utils.advanced_optimizer import AdvancedOptimizer
    from utils.quality_analyzer import QualityAnalyzer
    from utils.text_humanizer import TextHumanizer
    from utils.style_optimizer import StyleOptimizer
    from utils import LLMClient
    
    data = request.json
    chapter_numbers = data.get('chapter_numbers', [])
    
    try:
        # 如果未指定章节，则优化所有章节
        if not chapter_numbers:
            all_chapters = storage.get_all_chapters()
            chapter_numbers = [ch.get('chapter_number', i) for i, ch in enumerate(all_chapters, 1)]
        
        if not chapter_numbers:
            return jsonify({'success': False, 'message': '没有可优化的章节'})
        
        # 初始化优化器
        orchestrator = AgentOrchestrator()
        advanced_optimizer = AdvancedOptimizer()
        quality_analyzer = QualityAnalyzer()
        text_humanizer = TextHumanizer(LLMClient())
        style_optimizer = StyleOptimizer(LLMClient())
        
        results = []
        optimized_count = 0
        
        for chapter_num in chapter_numbers:
            chapter = storage.load_chapter(chapter_num)
            if not chapter:
                results.append({
                    'chapter': chapter_num,
                    'status': 'failed',
                    'error': '章节不存在'
                })
                continue
            
            content = chapter.get('content', '')
            if not content:
                results.append({
                    'chapter': chapter_num,
                    'status': 'skipped',
                    'reason': '章节内容为空'
                })
                continue
            
            try:
                # 步骤1：质量分析
                quality_before = quality_analyzer.analyze(content)
                
                # 步骤2：高级优化
                context = orchestrator.context_manager.get_full_context()
                opt_result = advanced_optimizer.comprehensive_optimize(content, context)
                
                if opt_result['optimization_success']:
                    content = opt_result['optimized_content']
                    improvements = opt_result['improvements']
                else:
                    improvements = []
                
                # 步骤3：人性化处理
                humanize_result = text_humanizer.humanize(content, aggressive=True)
                content = humanize_result.get('humanized_text', content)
                
                # 步骤4：风格优化
                style_result = style_optimizer.optimize(content, {
                    'vivid_description': True,
                    'dialogue_variation': True,
                    'rhythm_adjustment': True
                })
                content = style_result.get('optimized_text', content)
                
                # 步骤5：质量复评
                quality_after = quality_analyzer.analyze(content)
                
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
                    
                    results.append({
                        'chapter': chapter_num,
                        'status': 'success',
                        'quality_before': quality_before['overall_score'],
                        'quality_after': quality_after['overall_score'],
                        'improvement': quality_after['overall_score'] - quality_before['overall_score'],
                        'improvements': improvements
                    })
                else:
                    results.append({
                        'chapter': chapter_num,
                        'status': 'skipped',
                        'reason': '质量已达标',
                        'quality_score': quality_before['overall_score']
                    })
                
            except Exception as e:
                logger.error(f"优化第{chapter_num}章失败: {e}")
                results.append({
                    'chapter': chapter_num,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'data': {
                'total_chapters': len(chapter_numbers),
                'optimized_count': optimized_count,
                'skipped_count': len([r for r in results if r['status'] == 'skipped']),
                'failed_count': len([r for r in results if r['status'] == 'failed']),
                'results': results
            }
        })
        
    except Exception as e:
        logger.error(f"一条龙优化失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/optimize/single', methods=['POST'])
def optimize_single_chapter():
    """优化单个章节"""
    from agents.agent_orchestrator import AgentOrchestrator
    from utils.advanced_optimizer import AdvancedOptimizer
    from utils.quality_analyzer import QualityAnalyzer
    from utils.text_humanizer import TextHumanizer
    from utils.style_optimizer import StyleOptimizer
    from utils import LLMClient
    
    data = request.json
    chapter_number = data.get('chapter_number')
    
    if not chapter_number:
        return jsonify({'success': False, 'message': '请指定章节号'})
    
    try:
        chapter = storage.load_chapter(chapter_number)
        if not chapter:
            return jsonify({'success': False, 'message': f'未找到第{chapter_number}章'})
        
        content = chapter.get('content', '')
        if not content:
            return jsonify({'success': False, 'message': '章节内容为空'})
        
        # 初始化优化器
        orchestrator = AgentOrchestrator()
        advanced_optimizer = AdvancedOptimizer()
        quality_analyzer = QualityAnalyzer()
        text_humanizer = TextHumanizer(LLMClient())
        style_optimizer = StyleOptimizer(LLMClient())
        
        # 5步优化流程
        steps = []
        
        # 步骤1：质量分析
        quality_before = quality_analyzer.analyze(content)
        steps.append({
            'step': 1,
            'name': '质量分析',
            'status': 'completed',
            'result': f"质量评分: {quality_before['overall_score']:.1f}/10"
        })
        
        # 步骤2：高级优化
        context = orchestrator.context_manager.get_full_context()
        opt_result = advanced_optimizer.comprehensive_optimize(content, context)
        
        if opt_result['optimization_success']:
            content = opt_result['optimized_content']
            improvements = opt_result['improvements']
            steps.append({
                'step': 2,
                'name': '高级内容优化',
                'status': 'completed',
                'result': f"改进: {', '.join(improvements[:2])}"
            })
        else:
            steps.append({
                'step': 2,
                'name': '高级内容优化',
                'status': 'skipped',
                'result': '无需优化'
            })
            improvements = []
        
        # 步骤3：人性化处理
        humanize_result = text_humanizer.humanize(content, aggressive=True)
        content = humanize_result.get('humanized_text', content)
        steps.append({
            'step': 3,
            'name': '人性化优化',
            'status': 'completed',
            'result': '已完成'
        })
        
        # 步骤4：风格优化
        style_result = style_optimizer.optimize(content, {
            'vivid_description': True,
            'dialogue_variation': True,
            'rhythm_adjustment': True
        })
        content = style_result.get('optimized_text', content)
        steps.append({
            'step': 4,
            'name': '风格优化',
            'status': 'completed',
            'result': '已完成'
        })
        
        # 步骤5：质量复评
        quality_after = quality_analyzer.analyze(content)
        steps.append({
            'step': 5,
            'name': '质量复评',
            'status': 'completed',
            'result': f"质量评分: {quality_after['overall_score']:.1f}/10"
        })
        
        # 保存优化结果
        if quality_after['overall_score'] > quality_before['overall_score']:
            storage.update_chapter(chapter_number, {
                'content': content,
                'word_count': len(content),
                'optimized_by_pipeline': True,
                'quality_before': quality_before['overall_score'],
                'quality_after': quality_after['overall_score']
            })
            
            return jsonify({
                'success': True,
                'data': {
                    'chapter_number': chapter_number,
                    'quality_before': quality_before['overall_score'],
                    'quality_after': quality_after['overall_score'],
                    'improvement': quality_after['overall_score'] - quality_before['overall_score'],
                    'improvements': improvements,
                    'steps': steps,
                    'optimized_content': content
                }
            })
        else:
            return jsonify({
                'success': True,
                'data': {
                    'chapter_number': chapter_number,
                    'quality_score': quality_before['overall_score'],
                    'skipped': True,
                    'reason': '质量已达标，无需优化',
                    'steps': steps
                }
            })
        
    except Exception as e:
        logger.error(f"优化第{chapter_number}章失败: {e}")
        return jsonify({'success': False, 'message': str(e)})

def run_app():
    """运行Web应用"""
    host = config.get('web.host', '0.0.0.0')
    port = config.get('web.port', 5000)
    debug = config.get('web.debug', False)

    # 启动系统监控
    system_monitor.start()
    logger.info("系统监控已启动")

    # 启动调度器
    if config.get('scheduler.enabled', True):
        scheduler.start()
        logger.info("调度器已启动")

    print(f"\n{'=' * 60}")
    print(f"小说生成系统Web界面已启动")
    print(f"访问地址: http://localhost:{port}")
    print(f"{'=' * 60}\n")

    logger.info(f"Web应用启动，监听 {host}:{port}")

    try:
        app.run(host=host, port=port, debug=debug)
    finally:
        # 清理资源
        logger.info("正在关闭应用...")
        system_monitor.stop()
        scheduler.stop()
        from utils import LLMClient
        LLMClient.shutdown()
        logger.info("应用已关闭")

if __name__ == '__main__':
    run_app()
