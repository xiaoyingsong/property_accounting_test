# fixtures/login_fixture.py
import pytest
import allure
from playwright.sync_api import Page, expect
from config.config import BASE_URL, GLOBAL_TIMEOUT
from config.login_data import DEFAULT_LOGIN_DATA
from fixtures.browser_fixture import playwright_page
from utils.log_utils import logger
from utils.captcha_utils import get_slider_gap, drag_slider_human  # 引入滑块工具函数

@pytest.fixture(scope="function")
def login_success_page(playwright_page: Page) -> Page:
    page = playwright_page
    logger.info("=== 开始执行登录Fixture ===")

    with allure.step("Fixture：执行登录流程"):
        try:
            # 1. 切换语言（增加显式等待，提升稳定性）
            lang_btn = page.get_by_role("button", name="English")
            lang_btn.wait_for(state="enabled", timeout=GLOBAL_TIMEOUT)
            lang_btn.click()
            page.get_by_role("menuitem", name="简体中文").click()
            logger.info("切换语言为简体中文")

            # 2. 切换邮箱登录
            email_tab = page.get_by_role("tab", name="邮箱登录")
            email_tab.wait_for(state="enabled", timeout=GLOBAL_TIMEOUT)
            email_tab.click()
            logger.info("切换到邮箱登录标签页")

            # 3. 输入登录数据
            email_panel = page.locator("#pane-email")
            email_panel.wait_for(timeout=GLOBAL_TIMEOUT)
            email_panel.get_by_placeholder("example@7link.com").fill(DEFAULT_LOGIN_DATA["email"])
            email_panel.get_by_placeholder("请输入密码").fill(DEFAULT_LOGIN_DATA["password"])
            if DEFAULT_LOGIN_DATA["remember_me"]:
                email_panel.get_by_label("记住我").check()
            logger.info("输入账号密码（管理员账号）")

            # 4. 点击登录
            login_btn = page.get_by_role("button", name="登录")
            login_btn.wait_for(state="enabled", timeout=GLOBAL_TIMEOUT)
            login_btn.click()
            logger.info("点击登录按钮")

            # ========== 新增：滑块验证码处理（核心） ==========
            with allure.step("处理滑块拼图验证码"):
                # 等待验证码弹窗出现
                captcha_dialog = page.get_by_text("请完成安全验证")
                captcha_dialog.wait_for(state="visible", timeout=GLOBAL_TIMEOUT)
                logger.info("检测到滑块验证码弹窗")

                # 识别缺口位置（⚠️ 替换为你页面实际的验证码图片定位器）
                # 示例：page.locator("div[role='dialog'] >> css=img") 可根据F12的HTML结构调整
                gap_x = get_slider_gap(page, "div[role='dialog'] >> css=img")
                logger.info(f"识别到缺口位置，需拖动距离：{gap_x}px")

                # 模拟人类拖动滑块（⚠️ 替换为你页面实际的滑块定位器）
                drag_slider_human(page, "div[role='dialog'] >> css=.slider-btn", gap_x)
                logger.info("完成滑块拖动")

                # 等待验证成功，弹窗消失
                captcha_dialog.wait_for(state="hidden", timeout=GLOBAL_TIMEOUT)
                logger.info("滑块验证成功，弹窗关闭")
            # ========== 滑块处理结束 ==========

            # 5. 验证登录成功（补全显性断言，避免假登录）
            page.wait_for_url(f"{BASE_URL}/index", timeout=GLOBAL_TIMEOUT)
            expect(page).to_have_url(f"{BASE_URL}/index", timeout=GLOBAL_TIMEOUT)
            expect(page.get_by_role("heading", name="首页")).to_be_visible(timeout=GLOBAL_TIMEOUT)
            logger.info("✅ 登录成功，进入首页")
            allure.attach(page.screenshot(full_page=True), name="登录成功首页", attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            logger.error(f"❌ 登录流程执行失败：{str(e)}")
            allure.attach(str(e), name="登录失败异常信息", attachment_type=allure.attachment_type.TEXT)
            allure.attach(page.screenshot(full_page=True), name="登录失败截图", attachment_type=allure.attachment_type.PNG)
            raise e

    yield page

    # 后置清理：退出登录
    with allure.step("Fixture：后置清理-退出登录"):
        try:
            page.get_by_role("button", name="用户头像").click()
            page.get_by_role("menuitem", name="退出登录").click()
            page.wait_for_url(f"{BASE_URL}/login", timeout=GLOBAL_TIMEOUT)
            logger.info("✅ Fixture后置清理：退出登录成功")
        except Exception as e:
            logger.error(f"❌ Fixture后置清理失败：{str(e)}")
            allure.attach(page.screenshot(full_page=True), name="退出登录失败截图", attachment_type=allure.attachment_type.PNG)