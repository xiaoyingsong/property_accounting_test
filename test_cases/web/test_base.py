# test_cases/test_housing_unit.py
import pytest
import allure
from playwright.sync_api import Page
from config.config import BASE_URL, GLOBAL_TIMEOUT
from fixtures.login_fixture import login_success_page
from fixtures.browser_fixture import playwright_page,playwright_browser
from pages.project_setting_center_page import HomePage
from pages.housing_unit_list_page import HousingUnitFormPage
from pages.housing_unit_form_page import HousingUnitListPage
from utils.log_utils import logger

@pytest.mark.smoke
@pytest.mark.project
def test_tc_p0_smoke_add_housing_unit_success(login_success_page: Page):
    """
    用例名称: tc-p0-冒烟测试:新增房屋单元提交成功
    前置条件:
        pc: 已通过有效账号登录系统并成功进入首页
        pc: 左侧导航栏"项目设置中心"可点击
        pc: 系统已配置可用楼栋数据（如Block A）appium-doctor --android
    """
    page = login_success_page
    logger.info("=== 开始执行冒烟用例：新增房屋单元提交成功 ===")

    # 1. 初始化页面对象
    home_page = HomePage(page)
    list_page = HousingUnitListPage(page)
    form_page = HousingUnitFormPage(page)

    # 2. 执行业务流程
    home_page.click_project_setting()  # 点击项目设置中心
    home_page.click_housing_unit()      # 点击房屋单元
    logger.info("=== 冒烟用例执行完成：新增房屋单元提交成功 ===")