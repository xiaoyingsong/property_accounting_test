import logging
import os
from datetime import datetime

def setup_logger(name="property_test", log_level=logging.INFO):
    """配置全局日志，同时输出到控制台和文件"""
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 避免重复添加Handler
    if not logger.handlers:
        # 控制台输出Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # 文件输出Handler（按日期生成日志文件）
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}_test.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level)

        # 日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# 全局日志实例，供所有用例和Fixture使用
logger = setup_logger()