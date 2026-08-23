"""小说生成自动调度器 - 增强版
支持：
- 并发章节生成
- 任务队列管理
- 失败重试机制
- 性能监控
"""
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, Empty
from threading import Lock
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from agents import OutlineAgent, ChapterPlanningAgent, ContentGenerationAgent
from agents.human_like_generator import HumanLikeGenerator
from utils import Storage, config, get_logger, perf_logger, LLMClient

# 配置日志
logger = get_logger('scheduler')

class NovelScheduler:
    """小说生成调度器 - 增强版"""

    def __init__(self, max_workers: int = 3):
        self.scheduler = BackgroundScheduler()
        self.storage = Storage()
        self.outline_agent = OutlineAgent()
        self.planning_agent = ChapterPlanningAgent()
        self.generation_agent = ContentGenerationAgent()

        # 从配置加载调度设置
        self.schedule_time = config.get('scheduler.schedule_time', '09:00')
        self.chapters_per_day = config.get('scheduler.chapters_per_day', 2)
        self.enabled = config.get('scheduler.enabled', True)

        # 线程池配置
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="chapter_gen"
        )

        # 任务队列
        self.task_queue = Queue()
        self.task_lock = Lock()

        # 统计信息
        self.stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'total_chapters': 0
        }

        logger.info(f"调度器初始化完成，最大并发数: {max_workers}")
    
    def start(self):
        """启动调度器"""
        if not self.enabled:
            logger.warning("调度器未启用")
            print("调度器未启用")
            return

        # 解析调度时间
        hour, minute = map(int, self.schedule_time.split(':'))

        # 添加定时任务
        self.scheduler.add_job(
            self.daily_generation_task,
            trigger=CronTrigger(hour=hour, minute=minute),
            id='daily_novel_generation',
            name='每日小说生成任务',
            replace_existing=True
        )

        self.scheduler.start()
        logger.info(f"调度器已启动，每日 {self.schedule_time} 自动生成 {self.chapters_per_day} 章")
        print(f"✓ 调度器已启动，每日 {self.schedule_time} 自动生成 {self.chapters_per_day} 章")

    def stop(self):
        """停止调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("调度器已停止")
            print("✓ 调度器已停止")

        # 关闭线程池
        self.executor.shutdown(wait=True)
        logger.info("线程池已关闭")
    
    def _generate_single_chapter_task(self, chapter_number: int, outline: Dict) -> Optional[Dict]:
        """
        生成单个章节的任务（用于并发执行）

        Args:
            chapter_number: 章节编号
            outline: 小说大纲

        Returns:
            章节数据或None
        """
        start_time = time.time()

        try:
            logger.info(f"开始生成第 {chapter_number} 章")
            print(f"\n[线程] 开始生成第 {chapter_number} 章...")

            # 规划章节
            chapter_plan = self.planning_agent.plan_chapter(chapter_number, outline)
            if not chapter_plan:
                logger.error(f"第 {chapter_number} 章规划失败")
                print(f"✗ 第 {chapter_number} 章规划失败")
                return None

            # 生成内容（根据配置决定是否走人性化高质量管线）
            chapter_data = None
            try:
                if config.get('humanize.enabled', True):
                    quality_mode = str(config.get('humanize.mode', 'high')).lower()
                    hl_generator = HumanLikeGenerator(LLMClient())
                    result = hl_generator.generate_human_like_chapter(
                        chapter_plan=chapter_plan,
                        previous_context=None,
                        quality_mode=quality_mode
                    )
                    chapter_data = {
                        'chapter_number': chapter_number,
                        'title': chapter_plan.get('chapter_title', f'第{chapter_number}章'),
                        'content': result['final_content'],
                        'plan': chapter_plan,
                        'word_count': len(result['final_content']),
                        'quality': result.get('final_quality', {})
                    }
                    self.storage.save_chapter(chapter_number, chapter_data)
                else:
                    chapter_data = self.generation_agent.generate_chapter(chapter_number, chapter_plan, outline)
            except Exception as gen_e:
                logger.error(f"第 {chapter_number} 章生成异常: {gen_e}")
                chapter_data = None

            if chapter_data:
                elapsed_time = time.time() - start_time
                perf_logger.log_operation(
                    f"generate_chapter_{chapter_number}",
                    elapsed_time,
                    success=True,
                    word_count=chapter_data.get('word_count', 0)
                )
                logger.info(f"第 {chapter_number} 章生成成功，耗时: {elapsed_time:.2f}秒")
                print(f"✓ 第 {chapter_number} 章生成成功")
                return chapter_data
            else:
                elapsed_time = time.time() - start_time
                perf_logger.log_operation(f"generate_chapter_{chapter_number}", elapsed_time, success=False)
                logger.error(f"第 {chapter_number} 章生成失败")
                print(f"✗ 第 {chapter_number} 章生成失败")
                return None

        except Exception as e:
            elapsed_time = time.time() - start_time
            perf_logger.log_operation(f"generate_chapter_{chapter_number}", elapsed_time, success=False)
            logger.error(f"第 {chapter_number} 章生成异常: {e}", exc_info=True)
            print(f"✗ 第 {chapter_number} 章生成异常: {e}")
            return None

    def generate_chapters_concurrent(self, chapter_numbers: List[int], outline: Dict) -> Dict[int, Optional[Dict]]:
        """
        并发生成多个章节

        Args:
            chapter_numbers: 章节编号列表
            outline: 小说大纲

        Returns:
            章节编号到章节数据的映射
        """
        logger.info(f"开始并发生成 {len(chapter_numbers)} 个章节")
        print(f"\n并发生成 {len(chapter_numbers)} 个章节...")

        results = {}
        futures = {}

        # 提交任务
        for chapter_num in chapter_numbers:
            future = self.executor.submit(self._generate_single_chapter_task, chapter_num, outline)
            futures[future] = chapter_num

        # 等待完成
        for future in as_completed(futures):
            chapter_num = futures[future]
            try:
                result = future.result()
                results[chapter_num] = result
            except Exception as e:
                logger.error(f"章节 {chapter_num} 生成任务异常: {e}")
                results[chapter_num] = None

        success_count = sum(1 for r in results.values() if r is not None)
        logger.info(f"并发生成完成，成功: {success_count}/{len(chapter_numbers)}")

        return results

    def daily_generation_task(self):
        """每日生成任务（支持并发）"""
        start_time = time.time()

        print("\n" + "=" * 60)
        print(f"每日生成任务开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        logger.info("每日生成任务开始")

        try:
            # 检查是否有大纲
            outline = self.storage.load_outline()
            if not outline:
                logger.info("未找到大纲，开始创建大纲")
                print("未找到大纲，开始创建大纲...")
                mode = config.get('creation_mode.mode', 'autonomous')
                outline = self.outline_agent.create_outline(mode=mode)
                if not outline:
                    logger.error("大纲创建失败")
                    print("✗ 大纲创建失败，任务终止")
                    return

            # 获取当前进度
            latest_chapter = self.storage.get_latest_chapter_number()
            total_chapters = len(outline.get('chapter_outline', []))

            logger.info(f"当前进度: {latest_chapter}/{total_chapters} 章")
            print(f"\n当前进度: {latest_chapter}/{total_chapters} 章")

            # 确定要生成的章节
            chapters_to_generate = []
            for i in range(self.chapters_per_day):
                next_chapter = latest_chapter + i + 1
                if next_chapter <= total_chapters:
                    chapters_to_generate.append(next_chapter)
                else:
                    print(f"\n所有章节已生成完毕！")
                    break

            if not chapters_to_generate:
                logger.info("没有需要生成的章节")
                return

            # 并发生成章节
            results = self.generate_chapters_concurrent(chapters_to_generate, outline)

            # 统计结果
            chapters_generated = sum(1 for r in results.values() if r is not None)

            # 更新统计
            with self.task_lock:
                self.stats['total_tasks'] += 1
                self.stats['completed_tasks'] += 1
                self.stats['total_chapters'] += chapters_generated

            elapsed_time = time.time() - start_time
            perf_logger.log_operation('daily_generation_task', elapsed_time, success=True, chapters=chapters_generated)

            print("\n" + "=" * 60)
            print(f"每日生成任务完成 - 成功生成 {chapters_generated}/{len(chapters_to_generate)} 章")
            print(f"总耗时: {elapsed_time:.2f}秒")
            print("=" * 60)

            logger.info(f"每日生成任务完成，成功: {chapters_generated}/{len(chapters_to_generate)} 章，耗时: {elapsed_time:.2f}秒")

        except Exception as e:
            elapsed_time = time.time() - start_time
            perf_logger.log_operation('daily_generation_task', elapsed_time, success=False)

            with self.task_lock:
                self.stats['total_tasks'] += 1
                self.stats['failed_tasks'] += 1

            logger.error(f"每日生成任务出错: {e}", exc_info=True)
            print(f"\n✗ 每日生成任务出错: {e}")
            import traceback
            traceback.print_exc()
    
    def manual_trigger(self):
        """手动触发生成任务"""
        logger.info("手动触发生成任务")
        print("手动触发生成任务...")
        self.daily_generation_task()

    def generate_single_chapter(self):
        """生成单个章节（用于测试或手动补充）"""
        outline = self.storage.load_outline()
        if not outline:
            logger.warning("未找到大纲")
            print("✗ 未找到大纲")
            return None

        latest_chapter = self.storage.get_latest_chapter_number()
        next_chapter = latest_chapter + 1

        logger.info(f"开始生成第 {next_chapter} 章")
        print(f"开始生成第 {next_chapter} 章...")

        return self._generate_single_chapter_task(next_chapter, outline)

    def update_schedule(self, schedule_time=None, chapters_per_day=None):
        """更新调度设置"""
        if schedule_time:
            self.schedule_time = schedule_time
            config.set('scheduler.schedule_time', schedule_time)
            logger.info(f"更新调度时间: {schedule_time}")

        if chapters_per_day:
            self.chapters_per_day = chapters_per_day
            config.set('scheduler.chapters_per_day', chapters_per_day)
            logger.info(f"更新每日章节数: {chapters_per_day}")

        config.save()

        # 重启调度器以应用新设置
        if self.scheduler.running:
            self.stop()
            self.start()

        print(f"✓ 调度设置已更新: {self.schedule_time}, {self.chapters_per_day}章/天")

    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self.task_lock:
            return self.stats.copy()

    def __del__(self):
        """析构函数，确保资源释放"""
        try:
            self.executor.shutdown(wait=False)
        except:
            pass
