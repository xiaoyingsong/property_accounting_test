import pytest
import allure
from utils.db_utils import query_bill_info, update_bill_status

@pytest.mark.payment
@pytest.mark.critical
class TestPaymentModule:
    """支付管理模块测试用例，区分自研/第三方对接场景"""

    def test_payment_success_self_system(self, login, self_system_docking, db_cursor):
        """测试自研系统对接微信支付成功，核心用例"""
        page = login
        bill_id = "TEST20260304001"
        # 准备测试数据：确保账单为未支付状态
        update_bill_status(db_cursor, bill_id, "unpaid", "self_system")

        with allure.step("步骤1：进入支付页面"):
            page.get_by_text("账单管理").click()
            page.get_by_text(bill_id).click()
            page.get_by_role("button", name="支付").click()
        with allure.step("步骤2：选择微信支付，确认支付"):
            page.get_by_text("微信支付").click()
            page.get_by_role("button", name="确认支付").click()
            # 等待支付成功跳转
            page.wait_for_url(f"{TEST_URL}/bill/detail/{bill_id}", timeout=10000)
        with allure.step("步骤3：验证支付状态"):
            assert page.get_by_text("已支付").is_visible(), "支付成功状态未显示"
            # 数据库校验
            bill_info = query_bill_info(db_cursor, bill_id, "self_system")
            assert bill_info["pay_status"] == "paid", "数据库支付状态未同步"
        allure.attach(page.screenshot(), name="支付成功页面", attachment_type=allure.attachment_type.PNG)

    def test_payment_fail_third_party(self, login, third_party_docking, db_cursor):
        """测试第三方系统对接支付失败，容错处理"""
        page = login
        bill_id = "TEST20260304002"
        bill_data = {
            "bill_id": bill_id,
            "property_id": "PROP002",
            "amount": 200.50,
            "docking_type": "third_party"
        }
        # 同步账单至第三方系统
        third_party_docking(bill_data)
        # 准备测试数据：未支付状态
        update_bill_status(db_cursor, bill_id, "unpaid", "third_party")

        with allure.step("步骤1：进入支付页面"):
            page.get_by_text("账单管理").click()
            page.get_by_text(bill_id).click()
            page.get_by_role("button", name="支付").click()
        with allure.step("步骤2：选择支付宝，模拟支付失败"):
            page.get_by_text("支付宝").click()
            page.get_by_role("button", name="确认支付").click()
            # 模拟支付失败（拦截接口返回失败）
            page.get_by_text("支付失败，点击重试").click()
        with allure.step("步骤3：验证容错处理"):
            assert page.get_by_text("未支付").is_visible(), "支付失败后状态异常"
            # 数据库校验
            bill_info = query_bill_info(db_cursor, bill_id, "third_party")
            assert bill_info["pay_status"] == "unpaid", "数据库状态同步错误"
        allure.attach(page.screenshot(), name="支付失败页面", attachment_type=allure.attachment_type.PNG)