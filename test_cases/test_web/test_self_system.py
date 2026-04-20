import pytest
import allure
from utils.api_utils import query_sync_status

@pytest.mark.self_system
@pytest.mark.critical
class TestSelfSystemDocking:
    """自研系统对接测试用例（优先执行），覆盖核心对接场景"""

    def test_self_system_bill_sync(self, login, self_system_docking, db_cursor):
        """测试自研系统账单同步成功，核心对接用例"""
        page = login
        bill_data = {
            "bill_id": "TEST20260304003",
            "property_id": "PROP003",
            "amount": 500.00,
            "period": "2026-03",
            "docking_type": "self_system"
        }
        with allure.step("步骤1：自研系统触发账单同步"):
            resp = self_system_docking(bill_data)
            assert resp["code"] == 200, f"账单同步失败：{resp['msg']}"
            assert resp["data"]["sync_status"] == 1, "同步状态异常"
        with allure.step("步骤2：查询同步状态，二次校验"):
            sync_status = query_sync_status(bill_data["bill_id"], "self_system")
            assert sync_status == 1, "同步状态查询异常"
        with allure.step("步骤3：数据库校验同步状态"):
            bill_info = query_bill_info(db_cursor, bill_data["bill_id"], "self_system")
            assert bill_info["sync_status"] == 1, "数据库同步状态未更新"
        allure.attach(str(resp), name="同步响应数据", attachment_type=allure.attachment_type.TEXT)

    def test_self_system_api_timeout(self, login, self_system_docking, monkeypatch):
        """测试自研系统接口超时，容错处理"""
        page = login
        bill_data = {
            "bill_id": "TEST20260304005",
            "property_id": "PROP005",
            "amount": 800.00,
            "docking_type": "self_system"
        }

        # 模拟接口超时
        def mock_sync_bill(*args, **kwargs):
            raise Exception("请求超时：connect timed out")

        with allure.step("步骤1：模拟自研系统接口超时"):
            monkeypatch.setattr("utils.api_utils.sync_bill_to_self_system", mock_sync_bill)
            with pytest.raises(Exception) as excinfo:
                self_system_docking(bill_data)
            assert "请求超时" in str(excinfo.value), "超时异常未捕获"
        with allure.step("步骤2：验证系统容错提示"):
            assert page.get_by_text("对接超时，请重试").is_visible(), "超时容错提示未显示"
        allure.attach(page.screenshot(), name="接口超时页面", attachment_type=allure.attachment_type.PNG)