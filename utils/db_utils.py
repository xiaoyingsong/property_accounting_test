import pymysql
from config.config import DB_CONFIG
from utils.log_utils import logger

def query_bill_info(cursor, bill_id, docking_type):
    """查询账单信息，区分自研/第三方对接场景，用于数据校验（适配马来西亚货币规则）"""
    try:
        sql = "SELECT bill_id, amount, pay_status, sync_status, pay_time, docking_type FROM bill_info WHERE bill_id = %s AND docking_type = %s"
        cursor.execute(sql, (bill_id, docking_type))
        result = cursor.fetchone()
        if not result:
            logger.error(f"账单不存在：bill_id={bill_id}，对接场景={docking_type}")
            raise ValueError(f"账单不存在：bill_id={bill_id}，对接场景={docking_type}")
        logger.info(f"查询账单成功：bill_id={bill_id}，金额={result['amount']}，对接场景={docking_type}")
        return result
    except Exception as e:
        logger.error(f"查询账单失败：{str(e)}，对接场景={docking_type}")
        raise

def update_bill_status(cursor, bill_id, pay_status, docking_type):
    """更新账单支付状态，区分自研/第三方对接场景，用于测试数据准备"""
    try:
        sql = "UPDATE bill_info SET pay_status = %s WHERE bill_id = %s AND docking_type = %s"
        cursor.execute(sql, (pay_status, bill_id, docking_type))
        logger.info(f"更新账单状态成功：bill_id={bill_id}，pay_status={pay_status}，对接场景={docking_type}")
    except Exception as e:
        logger.error(f"更新账单状态失败：{str(e)}，对接场景={docking_type}")
        raise

def clear_test_data(cursor, docking_type=None):
    """清理测试数据，可按对接场景清理，避免数据冲突"""
    try:
        if docking_type:
            sql = "DELETE FROM bill_info WHERE docking_type = %s AND bill_id LIKE 'TEST%%'"
            cursor.execute(sql, (docking_type,))
            logger.info(f"清理{docking_type}测试数据成功")
        else:
            sql = "DELETE FROM bill_info WHERE bill_id LIKE 'TEST%%'"
            cursor.execute(sql)
            logger.info("清理所有测试账单数据成功")
    except Exception as e:
        logger.error(f"清理测试数据失败：{str(e)}")
        raise