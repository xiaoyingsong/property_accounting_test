# fixtures/login_fixture.py
import pytest
import allure
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from config.config import BASE_URL, GLOBAL_TIMEOUT
from config.login_data import DEFAULT_LOGIN_DATA  # 引入默认登录数据
from fixtures.web.browser_fixture import playwright_page
from utils.log_utils import logger
from utils.captcha_utils import get_slider_gap_candidates, drag_slider_human  # 引入滑块工具函数


def _refresh_captcha(page: Page) -> bool:
    """尝试点击验证码刷新按钮。"""
    refresh_selectors = [
        "#pane-email .verifybox .verify-sub-block .icon-refresh",
        "#pane-email .verifybox .verify-refresh",
        "#pane-email .verifybox [class*='refresh']",
    ]
    for selector in refresh_selectors:
        refresh_btn = page.locator(selector).first
        if refresh_btn.count() > 0 and refresh_btn.is_visible():
            refresh_btn.click(timeout=2000)
            page.wait_for_timeout(300)
            logger.info(f"已刷新滑块验证码: {selector}")
            return True
    logger.info("未找到可点击的验证码刷新按钮，继续下一次重试")
    return False


def _wait_captcha_passed(captcha) -> bool:
    """优先以验证码弹层隐藏作为通过判定。"""
    try:
        captcha.wait_for(state="hidden", timeout=4500)
        return True
    except PlaywrightTimeoutError:
        return False


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
        email_panel.get_by_placeholder("example@7link.com").fill(
            DEFAULT_LOGIN_DATA["email"]
        )
        email_panel.get_by_placeholder("请输入密码").fill(
            DEFAULT_LOGIN_DATA["password"]
        )
        if DEFAULT_LOGIN_DATA["remember_me"]:
            email_panel.get_by_label("记住我").check()
        logger.info("输入账号密码（管理员账号）")

        # 点击登录
        page.get_by_role("button", name="登录").click()
        logger.info("点击登录按钮")

        # 滑块安全验证
        with allure.step("滑块安全验证"):
            captcha = page.locator("#pane-email .verifybox")
            captcha.wait_for(state="visible", timeout=5000)
            logger.info("检测到滑块验证弹窗")

            img_loc = "#pane-email .verifybox .verify-img-panel img"
            slider_loc = "#pane-email .verifybox .verify-move-block"

            for i in range(3):
                try:
                    logger.info(f"第{i + 1}次滑块验证")
                    candidates = get_slider_gap_candidates(page, img_loc)
                    solved = False
                    for base_offset, conf, method in candidates:
                        fine_offsets = [base_offset, base_offset - 5, base_offset + 5]
                        for offset in fine_offsets:
                            if offset <= 0:
                                continue
                            logger.info(f"尝试滑块偏移: {offset}px (conf={conf:.2f}, method={method})")
                            drag_slider_human(page, slider_loc, offset)
                            if _wait_captcha_passed(captcha):
                                solved = True
                                logger.info("滑块验证通过")
                                break
                            _refresh_captcha(page)
                        if solved:
                            break

                    if solved:
                        break
                    raise RuntimeError("当前轮次滑块未通过")
                except Exception as e:
                    logger.warning(f"第{i + 1}次滑块验证失败")
                    allure.attach(
                        page.screenshot(full_page=True),
                        name=f"滑块验证失败_{i + 1}",
                        attachment_type=allure.attachment_type.PNG,
                    )

                    if i == 2:
                        logger.error("滑块验证三次全部失败")
                        allure.attach(
                            page.screenshot(full_page=True),
                            name="最终失败",
                            attachment_type=allure.attachment_type.PNG,
                        )
                        raise e
                    _refresh_captcha(page)
                    page.wait_for_timeout(1000)
        # 验证登录成功
        # page.wait_for_url(f"{BASE_URL}/index", timeout=GLOBAL_TIMEOUT)
        # expect(page.url).to_be(f"{BASE_URL}/index")
        logger.info("✅ 登录成功，进入首页")
        allure.attach(
            page.screenshot(),
            name="登录成功首页",
            attachment_type=allure.attachment_type.PNG,
        )

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
