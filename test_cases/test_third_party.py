import pytest
import allure
from utils.api_utils import query_sync_status

@pytest.mark.third_party
@pytest.mark.normal
class TestThirdPartyDocking:
    """第三方系统对接测试用例（次要执行）"""

    def test_third_party_bill_sync(self, login, third_party_docking, db_cursor):
        """测试第三方系统账单同步成功"""
        page = login
        bill_data = {
            "bill_id": "TEST20260304004",
            "property_id": "PROP004",
            "amount": 300.00,
            "period": "2026-03",
            "docking_type": "third_party"
        }
        with allure.step("步骤1：第三方系统触发账单同步"):
            resp = third_party_docking(bill_data)
            assert resp["code"] == 200, f"账单同步失败：{resp['msg']}"
            assert resp["data"]["sync_status"] == 1, "同步状态异常"
        with allure.step("步骤2：查询同步状态"):
            sync_status = query_sync_status(bill_data["bill_id"], "third_party")
            assert sync_status == 1, "同步状态查询异常"
        allure.attach(str(resp), name="同步响应数据", attachment_type=allure.attachment_type.TEXT)

    def test_third_party_api_500(self, login, third_party_docking, monkeypatch):
        """测试第三方系统接口500异常，容错处理"""
        page = login
        bill_data = {
            "bill_id": "TEST20260304006",
            "property_id": "PROP006",
            "amount": 600.00,
            "docking_type": "third_party"
        }

        # 模拟接口500异常
        def mock_sync_bill(*args, **kwargs):
            raise Exception("服务器内部错误：500 Internal Server Error")

        with allure.step("步骤1：模拟第三方系统接口500异常"):
            monkeypatch.setattr("utils.api_utils.sync_bill_to_third_party", mock_sync_bill)
            with pytest.raises(Exception) as excinfo:
                third_party_docking(bill_data)
            assert "500" in str(excinfo.value), "500异常未捕获"
        with allure.step("步骤2：验证容错处理"):
            assert page.get_by_text("对接异常，请联系管理员").is_visible(), "500异常容错提示未显示"
        allure.attach(page.screenshot(), name="接口500异常页面", attachment_type=allure.attachment_type.PNG)