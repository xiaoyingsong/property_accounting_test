import pytest
import pymysql
from config.config import DB_CONFIG
from utils.log_utils import logger

@pytest.fixture(scope="session")
def db_connection():
    """数据库连接Fixture，全局复用，减少连接开销"""
    conn = None
    try:
        # 建立数据库连接（适配MySQL 8.0）
        conn = pymysql.connect(**DB_CONFIG)
        logger.info("数据库连接成功")
        yield conn
    except Exception as e:
        logger.error(f"数据库连接失败：{str(e)}")
        raise
    finally:
        # 关闭数据库连接
        if conn:
            conn.close()
            logger.info("数据库连接已关闭")

@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """数据库游标Fixture，用例独立，执行后回滚数据，避免影响其他用例"""
    cursor = db_connection.cursor(pymysql.cursors.DictCursor)
    try:
        yield cursor
        # 用例执行完成后回滚数据，避免测试数据污染
        db_connection.rollback()
    except Exception as e:
        logger.error(f"数据库操作失败：{str(e)}")
        db_connection.rollback()
        raise
    finally:
        # 关闭游标
        cursor.close()