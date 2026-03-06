# 项目设置中心菜单
import allure
from playwright.sync_api import Page, expect
from utils.log_utils import logger

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        # 元素定位器
        self.project_setting_menu = page.get_by_text("项目设置中心")
        self.housing_unit_menu = page.get_by_text("房屋单元")

    @allure.step("点击【项目设置中心】菜单")
    def click_project_setting(self):
        """点击项目设置中心，展开子菜单"""
        logger.info("点击【项目设置中心】菜单")
        expect(self.project_setting_menu).to_be_visible(timeout=5000)
        self.project_setting_menu.click()
        # 等待子菜单展开
        self.housing_unit_menu.wait_for(state="visible", timeout=5000)
        logger.info("✅ 项目设置中心子菜单已展开")
        allure.attach(self.page.screenshot(), name="项目设置中心子菜单", attachment_type=allure.attachment_type.PNG)

    @allure.step("点击【项目管理】子菜单")
    def click_housing_unit(self):
        """点击项目管理，进入列表页"""
        logger.info("点击【项目管理】子菜单")
        expect(self.housing_unit_menu).to_be_visible()
        self.housing_unit_menu.click()
        logger.info("✅ 成功进入项目管理列表页")

    @allure.step("点击【楼栋/街道设置】子菜单")
    def click_block_setting(self):
        """点击楼栋/街道设置，进入列表页"""
        logger.info("点击【楼栋/街道设置】子菜单")
        expect(self.housing_unit_menu).to_be_visible()
        self.housing_unit_menu.click()
        logger.info("✅ 成功进入楼栋/街道设置列表页")

    @allure.step("点击【平面图】子菜单")
    def click_floor_plan(self):
        """点击平面图，进入列表页"""
        logger.info("点击【平面图】子菜单")
        expect(self.housing_unit_menu).to_be_visible()
        self.housing_unit_menu.click()
        logger.info("✅ 成功进入平面图列表页")

    @allure.step("点击【房屋单元】子菜单")
    def click_housing_unit(self):
        """点击房屋单元，进入列表页"""
        logger.info("点击【房屋单元】子菜单")
        expect(self.housing_unit_menu).to_be_visible()
        self.housing_unit_menu.click()
        logger.info("✅ 成功进入房屋单元列表页")

    @allure.step("点击【申请列表】子菜单")
    def click_application_list(self):
        """点击申请列表设置，进入列表页"""
        logger.info("点击【申请列表】子菜单")
        expect(self.housing_unit_menu).to_be_visible()
        self.housing_unit_menu.click()
        logger.info("✅ 成功进入申请列表列表页")

    @allure.step("点击【公司管理】子菜单")
    def click_company_management(self):
        """点击公司管理，进入列表页"""
        logger.info("点击【公司管理】子菜单")
        expect(self.housing_unit_menu).to_be_visible()
        self.housing_unit_menu.click()
        logger.info("✅ 成功进入公司管理列表页")


