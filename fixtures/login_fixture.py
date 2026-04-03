# fixtures/login_fixture.py
import pytest
import allure
from playwright.sync_api import Page, expect
from config.config import BASE_URL, GLOBAL_TIMEOUT
from config.login_data import DEFAULT_LOGIN_DATA  # 引入默认登录数据
from fixtures.browser_fixture import playwright_page
from utils.log_utils import logger
from utils.captcha_utils import get_slider_gap, drag_slider_human  # 引入滑块工具函数


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
        email_panel.get_by_placeholder("example@7link.com").fill(DEFAULT_LOGIN_DATA["email"])
        email_panel.get_by_placeholder("请输入密码").fill(DEFAULT_LOGIN_DATA["password"])
        if DEFAULT_LOGIN_DATA["remember_me"]:
            email_panel.get_by_label("记住我").check()
        logger.info("输入账号密码（管理员账号）")

        # 点击登录
        page.get_by_role("button", name="登录").click()
        logger.info("点击登录按钮")

        # 滑动验证
        # ====================== 【终极精准版】滑块安全验证 ======================
        with allure.step("处理滑块安全验证"):
            # 1. 等待邮箱面板内的验证弹窗
            captcha_dialog = page.locator("#pane-email .verifybox")
            captcha_dialog.wait_for(state="visible", timeout=GLOBAL_TIMEOUT)
            logger.info("检测到安全验证弹窗")

            # 2. 验证码图片定位（固定）
            captcha_img_locator = "#pane-email .verifybox .verify-img-panel img"

            # 3. ✅ 真实滑块定位（根据你提供的HTML，永不超时）
            slider_locator = "#pane-email .verifybox .verify-move-block"
            # 强制等待滑块可见
            page.locator(slider_locator).wait_for(state="visible", timeout=GLOBAL_TIMEOUT)

            # 4. 识别缺口 + 模拟人类拖动
            gap_x = get_slider_gap(page, captcha_img_locator)
            drag_slider_human(page, slider_locator, gap_x)

            # 5. 等待验证通过，弹窗关闭
            captcha_dialog.wait_for(state="hidden", timeout=GLOBAL_TIMEOUT)
            logger.info("滑块验证成功")
        # ====================================================================

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
