# pages/home_page.py
import allure
from playwright.sync_api import Page, expect
from utils.log_utils import logger
from utils.locator_parser import parse_locator
from config.locators.web.home_locators import HOME_LOCATORS
from config.config import GLOBAL_TIMEOUT  # 全局超时配置

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        # 初始化定位器（无超时，仅定位）
        self.project_setting_menu = parse_locator(page, HOME_LOCATORS["project_setting_menu"])
        self.housing_unit_sub_menu = parse_locator(page, HOME_LOCATORS["housing_unit_sub_menu"])

    @allure.step("点击左侧【项目设置中心】菜单")
    def click_project_setting(self):
        logger.info("执行：点击项目设置中心菜单")
        # 断言元素可见时指定超时（核心！替代with_timeout）
        expect(self.project_setting_menu).to_be_visible(timeout=GLOBAL_TIMEOUT)
        self.project_setting_menu.click()
        # 等待子菜单展开时指定超时
        self.housing_unit_sub_menu.wait_for(state="visible", timeout=GLOBAL_TIMEOUT)
        logger.info("✅ 项目设置中心子菜单展开成功")
        allure.attach(self.page.screenshot(), name="项目设置中心子菜单", attachment_type=allure.attachment_type.PNG)

    @allure.step("点击【房屋单元】子菜单")
    def click_housing_unit(self):
        logger.info("执行：点击房屋单元子菜单")
        # 断言+超时
        expect(self.housing_unit_sub_menu).to_be_visible(timeout=GLOBAL_TIMEOUT)
        self.housing_unit_sub_menu.click()
        logger.info("✅ 进入房屋单元列表页成功")