import re
import time
import random
import datetime
from utils.log_utils import logger

def verify_malaysia_currency(amount):
    """验证马来西亚货币格式（保留2位小数，正数），适配马来西亚用户场景"""
    try:
        # 转换为浮点数，验证是否为正数
        amount_float = float(amount)
        if amount_float <= 0:
            logger.error(f"货币金额异常：{amount}，需为正数")
            return False
        # 验证是否保留2位小数
        if not re.match(r"^\d+\.\d{2}$", str(amount)):
            logger.error(f"货币格式异常：{amount}，需保留2位小数")
            return False
        logger.info(f"货币格式验证通过：{amount}")
        return True
    except Exception as e:
        logger.error(f"货币验证失败：{str(e)}")
        return False

def generate_test_bill_id(prefix="TEST"):
    """生成测试账单ID（格式：TEST+年月日+3位序号），用于测试数据准备"""
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    # 简单生成序号（实际可结合数据库自增序号优化）
    seq = random.randint(100, 999)
    bill_id = f"{prefix}{date_str}{seq}"
    logger.info(f"生成测试账单ID：{bill_id}")
    return bill_id

def sleep(seconds):
    """自定义睡眠函数，用于等待页面加载（替代time.sleep，便于统一管理）"""
    logger.info(f"等待{seconds}秒...")
    time.sleep(seconds)