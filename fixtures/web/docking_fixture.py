import pytest
from config.config import SELF_SYSTEM_API, THIRD_PARTY_API
from utils.api_utils import sync_bill_to_self_system, sync_bill_to_third_party
from utils.log_utils import logger

@pytest.fixture(scope="function")
def self_system_docking():
    """自研系统对接Fixture，提供自研系统同步等基础操作，优先使用"""
    def _sync_bill(bill_data):
        """同步账单至自研系统"""
        try:
            resp = sync_bill_to_self_system(bill_data)
            return resp
        except Exception as e:
            logger.error(f"自研系统对接失败：{str(e)}")
            raise
    yield _sync_bill

@pytest.fixture(scope="function")
def third_party_docking():
    """第三方系统对接Fixture，提供第三方系统同步等基础操作"""
    def _sync_bill(bill_data):
        """同步账单至第三方系统"""
        try:
            resp = sync_bill_to_third_party(bill_data)
            return resp
        except Exception as e:
            logger.error(f"第三方系统对接失败：{str(e)}")
            raise
    yield _sync_bill