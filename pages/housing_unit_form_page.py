# 房屋单元列表
import allure
from playwright.sync_api import Page, expect
from utils.log_utils import logger

class HousingUnitListPage:
    def __init__(self, page: Page):
        self.page = page
        # 元素定位器
        self.add_button = page.get_by_role("button", name="新增")
        self.page_title = page.get_by_role("heading", name="房屋单元管理")
        self.loading_mask = page.locator(".el-loading-mask")

    @allure.step("验证进入房屋单元列表页")
    def verify_list_page(self, test_url: str):
        """验证当前页面是房屋单元列表页"""
        expect(self.page.url).to_contain(f"{test_url}/housing-units", timeout=10000)
        expect(self.page_title).to_be_visible()
        allure.attach(self.page.screenshot(), name="房屋单元列表页", attachment_type=allure.attachment_type.PNG)

    @allure.step("点击【新增】按钮")
    def click_add_button(self):
        """点击新增按钮，打开表单页"""
        logger.info("点击【新增】按钮")
        expect(self.add_button).to_be_visible()
        self.add_button.click()
        # 等待表单加载，隐藏加载动画
        self.loading_mask.wait_for(state="hidden", timeout=5000)
        logger.info("✅ 成功打开新增房屋单元表单")