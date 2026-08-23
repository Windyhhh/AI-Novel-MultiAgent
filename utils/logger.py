"""
日志工具
提供统一的日志记录功能
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """获取或创建logger实例"""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # 控制台处理器 - 使用UTF-8编码
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    # 强制使用UTF-8编码
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    # 文件处理器
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime('%Y%m%d')
    log_file = log_dir / f'{name}_{today}.log'
    error_log_file = log_dir / f'{name}_error_{today}.log'
    
    # 普通日志文件 - 明确指定UTF-8编码
    file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    # 错误日志文件 - 明确指定UTF-8编码
    error_handler = logging.FileHandler(error_log_file, encoding='utf-8', mode='a')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger

class PerformanceLogger:
    """性能日志记录器"""
    def __init__(self):
        self.logger = get_logger('performance')
    
    def log_operation(self, operation: str, elapsed_time: float, success: bool = True, **kwargs):
        """记录操作性能"""
        status = "成功" if success else "失败"
        extra_info = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        msg = f"操作: {operation}, 状态: {status}, 耗时: {elapsed_time:.2f}秒"
        if extra_info:
            msg += f", {extra_info}"
        
        if success:
            self.logger.info(msg)
        else:
            self.logger.warning(msg)

# 全局性能日志实例
perf_logger = PerformanceLogger()
