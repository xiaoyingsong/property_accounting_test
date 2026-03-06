import pytest
import allure
from utils.db_utils import query_bill_info

@pytest.mark.bill
@pytest.mark.critical
class TestBillModule:
    """账单管理模块测试用例，优先覆盖自研系统对接场景"""

    def test_bill_create_self_system(self, login, self_system_docking, db_cursor):
        """测试自研系统触发生成账单，核心用例"""
        page = login
        # 构造账单数据（适配马来西亚货币规则，保留2位小数）
        bill_data = {
            "bill_id": "TEST20260304001",
            "property_id": "PROP001",
            "amount": 1000.00,
            "period": "2026-03",
            "docking_type": "self_system"
        }
        with allure.step("步骤1：自研系统同步账单"):
            resp = self_system_docking(bill_data)
            assert resp["code"] == 200, f"自研系统同步账单失败：{resp['msg']}"
            assert resp["data"]["sync_status"] == 1, "账单同步状态异常"
        with allure.step("步骤2：数据库校验账单存在"):
            bill_info = query_bill_info(db_cursor, bill_data["bill_id"], "self_system")
            assert bill_info["amount"] == bill_data["amount"], "账单金额不一致"
            assert bill_info["docking_type"] == "self_system", "对接场景标记错误"
        allure.attach(str(bill_info), name="账单数据", attachment_type=allure.attachment_type.TEXT)

    def test_bill_query(self, login, db_cursor):
        """测试账单查询功能（按账单ID查询）"""
        page = login
        bill_id = "TEST20260304001"
        with allure.step("步骤1：进入账单查询页面"):
            page.get_by_text("账单管理").click()
            page.get_by_text("账单查询").click()
        with allure.step("步骤2：输入账单ID查询"):
            page.get_by_label("账单ID").fill(bill_id)
            page.get_by_role("button", name="查询").click()
        with allure.step("步骤3：验证查询结果"):
            assert page.get_by_text(bill_id).is_visible(), "账单查询失败，未找到目标账单"
        allure.attach(page.screenshot(), name="账单查询结果", attachment_type=allure.attachment_type.PNG)