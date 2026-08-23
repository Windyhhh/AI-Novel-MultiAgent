"""系统监控模块
提供系统资源监控和性能统计
"""
import os
import time
import psutil
import threading
from typing import Dict, List
from datetime import datetime
from .logger import get_logger

logger = get_logger('monitor')


class SystemMonitor:
    """系统资源监控器"""
    
    def __init__(self, interval: int = 60):
        """
        初始化监控器
        
        Args:
            interval: 监控间隔（秒）
        """
        self.interval = interval
        self.running = False
        self.monitor_thread = None
        self.metrics_history = []
        self.max_history = 100  # 保留最近100条记录
        
        logger.info(f"系统监控器初始化，监控间隔: {interval}秒")
    
    def get_current_metrics(self) -> Dict:
        """获取当前系统指标"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # 内存使用情况
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            memory_total_mb = memory.total / (1024 * 1024)
            
            # 磁盘使用情况
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used_gb = disk.used / (1024 * 1024 * 1024)
            disk_total_gb = disk.total / (1024 * 1024 * 1024)
            
            # 进程信息
            process = psutil.Process(os.getpid())
            process_memory_mb = process.memory_info().rss / (1024 * 1024)
            process_cpu_percent = process.cpu_percent(interval=0.1)
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count
                },
                'memory': {
                    'percent': memory_percent,
                    'used_mb': round(memory_used_mb, 2),
                    'total_mb': round(memory_total_mb, 2)
                },
                'disk': {
                    'percent': disk_percent,
                    'used_gb': round(disk_used_gb, 2),
                    'total_gb': round(disk_total_gb, 2)
                },
                'process': {
                    'memory_mb': round(process_memory_mb, 2),
                    'cpu_percent': process_cpu_percent
                }
            }
            
            return metrics
        
        except Exception as e:
            logger.error(f"获取系统指标失败: {e}")
            return {}
    
    def _monitor_loop(self):
        """监控循环"""
        logger.info("监控循环开始")
        
        while self.running:
            try:
                metrics = self.get_current_metrics()
                
                if metrics:
                    # 添加到历史记录
                    self.metrics_history.append(metrics)
                    
                    # 限制历史记录数量
                    if len(self.metrics_history) > self.max_history:
                        self.metrics_history.pop(0)
                    
                    # 记录日志（仅在资源使用率较高时）
                    if metrics['cpu']['percent'] > 80 or metrics['memory']['percent'] > 80:
                        logger.warning(
                            f"资源使用率较高 - CPU: {metrics['cpu']['percent']}%, "
                            f"内存: {metrics['memory']['percent']}%"
                        )
                
                time.sleep(self.interval)
            
            except Exception as e:
                logger.error(f"监控循环出错: {e}")
                time.sleep(self.interval)
        
        logger.info("监控循环结束")
    
    def start(self):
        """启动监控"""
        if self.running:
            logger.warning("监控器已在运行")
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("系统监控已启动")
    
    def stop(self):
        """停止监控"""
        if not self.running:
            return
        
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("系统监控已停止")
    
    def get_metrics_history(self, count: int = 10) -> List[Dict]:
        """
        获取历史指标
        
        Args:
            count: 返回最近的记录数
        
        Returns:
            指标列表
        """
        return self.metrics_history[-count:]
    
    def get_summary(self) -> Dict:
        """获取监控摘要"""
        if not self.metrics_history:
            return {}
        
        # 计算平均值
        cpu_avg = sum(m['cpu']['percent'] for m in self.metrics_history) / len(self.metrics_history)
        memory_avg = sum(m['memory']['percent'] for m in self.metrics_history) / len(self.metrics_history)
        
        return {
            'records_count': len(self.metrics_history),
            'cpu_avg': round(cpu_avg, 2),
            'memory_avg': round(memory_avg, 2),
            'latest': self.metrics_history[-1] if self.metrics_history else None
        }


# 全局监控器实例
system_monitor = SystemMonitor(interval=60)

