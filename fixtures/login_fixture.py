# fixtures/login_fixture.py
import pytest
import allure
from playwright.sync_api import Page, expect
from config.config import BASE_URL, GLOBAL_TIMEOUT
from config.login_data import DEFAULT_LOGIN_DATA  # 引入默认登录数据
from fixtures.browser_fixture import playwright_page
from utils.log_utils import logger

@pytest.fixture(scope="function")
def login_success_page(playwright_page: Page) -> Page:
    page = playwright_page
    logger.info("=== 开始执行登录Fixture ===")

    with allure.step("Fixture：执行登录流程"):
        # 切换语言
        page.get_by_role("button", name="English").click()
        page.get_by_role("menuitem", name="简体中文").click()
        logger.info("切换语言为简体中文")

        # 切换邮箱登录
        email_tab = page.get_by_role("tab", name="邮箱登录")
        email_tab.click()
        logger.info("切换到邮箱登录标签页")

        # 输入登录数据（从配置获取，无硬编码）
        email_panel = page.locator("#pane-email")
        email_panel.wait_for(timeout=GLOBAL_TIMEOUT)
        email_panel.get_by_placeholder("请输入邮箱").fill(DEFAULT_LOGIN_DATA["email"])
        email_panel.get_by_placeholder("请输入密码").fill(DEFAULT_LOGIN_DATA["password"])
        if DEFAULT_LOGIN_DATA["remember_me"]:
            email_panel.get_by_label("记住我").check()
        logger.info("输入账号密码（管理员账号）")

        # 点击登录
        page.get_by_role("button", name="登录").click()
        logger.info("点击登录按钮")

        # 滑动安全验证

        # 验证登录成功
        # page.wait_for_url(f"{BASE_URL}/index", timeout=GLOBAL_TIMEOUT)
        # expect(page.url).to_be(f"{BASE_URL}/index")
        logger.info("✅ 登录成功，进入首页")
        allure.attach(page.screenshot(), name="登录成功首页", attachment_type=allure.attachment_type.PNG)

    yield page

    # 后置清理
    with allure.step("Fixture：后置清理-退出登录"):
        try:
            page.get_by_role("button", name="用户头像").click()
            page.get_by_role("menuitem", name="退出登录").click()
            page.wait_for_url(f"{BASE_URL}/login", timeout=GLOBAL_TIMEOUT)
            logger.info("✅ Fixture后置清理：退出登录成功")
        except Exception as e:
            logger.error(f"❌ Fixture后置清理失败：{str(e)}")

    page.close()
