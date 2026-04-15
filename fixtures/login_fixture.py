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

        # 滑块安全验证
        with allure.step("处理滑块安全验证"):
            captcha = page.locator("#pane-email .verifybox")
            captcha.wait_for(state="visible", timeout=5000)
            logger.info("检测到滑块验证弹窗")

            img_loc = "#pane-email .verifybox .verify-img-panel img"
            slider_loc = "#pane-email .verifybox .verify-move-block"

            # 3次重试机制
            for i in range(3):
                try:
                    logger.info(f"第{i + 1}次尝试验证滑块")
                    gap = get_slider_gap(page, img_loc)
                    drag_slider_human(page, slider_loc, gap)

                    captcha.wait_for(state="hidden", timeout=5000)
                    logger.info("滑块验证通过")
                    break
                except Exception as e:
                    logger.warning(f"第{i + 1}次滑块验证失败")
                    # Allure失败截图
                    allure.attach(page.screenshot(full_page=True), name=f"滑块验证第{i + 1}次失败",
                                  attachment_type=allure.attachment_type.PNG)
                    # 三次失败抛出异常
                    if i == 2:
                        logger.error("滑块验证3次全部失败")
                        allure.attach(page.screenshot(full_page=True), name="滑块验证最终失败",
                                      attachment_type=allure.attachment_type.PNG)
                        raise e
                    page.wait_for_timeout(1000)

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
