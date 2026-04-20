# conftest.py 测试失败自动截图
from pathlib import Path
from datetime import datetime
import re
import pytest
import allure
from playwright.sync_api import Page
from utils.log_utils import logger

ALLURE_RESULTS_DIR = Path(__file__).resolve().parent / "test_cases" / "allure-results"


def _safe_test_name(nodeid: str) -> str:
    safe = re.sub(r"[\\/:*?\"<>|]+", "_", nodeid)
    return safe.replace("::", "__")


def _save_screenshot_file(nodeid: str, screenshot: bytes, kind: str) -> Path:
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ts}_{kind}_{_safe_test_name(nodeid)}.png"
    file_path = ALLURE_RESULTS_DIR / filename
    file_path.write_bytes(screenshot)
    return file_path


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest 钩子函数：测试失败时自动截图
    作用：当用例失败/出错时，自动截取页面截图并附加到 Allure 报告
    """
    # 获取测试结果
    outcome = yield
    rep = outcome.get_result()

    # 仅在测试失败/出错时执行
    if rep.when == "call" and (rep.failed or rep.outcome == "failed"):
        logger.error(f"❌ 用例 {item.nodeid} 执行失败，开始自动截图")

        # 优先兼容 Web(Page) 与 App(Appium driver) 两类失败截图
        try:
            funcargs = getattr(item, "funcargs", {}) or {}
            test_name = item.nodeid.split("::")[-1]

            # 1) Web 场景：优先找已约定的 login_success_page
            page = funcargs.get("login_success_page")
            if isinstance(page, Page):
                screenshot = page.screenshot(full_page=True)
                file_path = _save_screenshot_file(item.nodeid, screenshot, "web")
                allure.attach(
                    screenshot,
                    name=f"失败截图(Web)-{test_name}",
                    attachment_type=allure.attachment_type.PNG,
                )
                logger.info(f"✅ Web失败截图已保存：{file_path}")
                logger.info(f"✅ Web失败截图已附加到 Allure 报告：{item.nodeid}")
                return

            # 2) Web 兜底：若参数中存在任意 Playwright Page，也进行截图
            for value in funcargs.values():
                if isinstance(value, Page):
                    screenshot = value.screenshot(full_page=True)
                    file_path = _save_screenshot_file(item.nodeid, screenshot, "web")
                    allure.attach(
                        screenshot,
                        name=f"失败截图(Web)-{test_name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
                    logger.info(f"✅ Web失败截图已保存：{file_path}")
                    logger.info(
                        f"✅ Web失败截图(兜底)已附加到 Allure 报告：{item.nodeid}"
                    )
                    return

            # 3) App 场景：使用 app_driver 或具备 get_screenshot_as_png 的对象
            app_driver = funcargs.get("app_driver")
            if app_driver and hasattr(app_driver, "get_screenshot_as_png"):
                screenshot = app_driver.get_screenshot_as_png()
                file_path = _save_screenshot_file(item.nodeid, screenshot, "app")
                allure.attach(
                    screenshot,
                    name=f"失败截图(App)-{test_name}",
                    attachment_type=allure.attachment_type.PNG,
                )
                logger.info(f"✅ App失败截图已保存：{file_path}")
                logger.info(f"✅ App失败截图已附加到 Allure 报告：{item.nodeid}")
                return

            for value in funcargs.values():
                if hasattr(value, "get_screenshot_as_png"):
                    screenshot = value.get_screenshot_as_png()
                    file_path = _save_screenshot_file(item.nodeid, screenshot, "app")
                    allure.attach(
                        screenshot,
                        name=f"失败截图(App)-{test_name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
                    logger.info(f"✅ App失败截图已保存：{file_path}")
                    logger.info(
                        f"✅ App失败截图(兜底)已附加到 Allure 报告：{item.nodeid}"
                    )
                    return

            logger.warning(f"⚠️ 未找到可截图对象（Page/app_driver）：{item.nodeid}")
        except Exception as e:
            logger.error(f"❌ 失败截图失败：{str(e)}")
            allure.attach(
                f"截图失败：{str(e)}",
                name="截图异常",
                attachment_type=allure.attachment_type.TEXT,
            )


pytest_plugins = [
    "fixtures.web.browser_fixture",  # 全局导入 Web 浏览器夹具
    "fixtures.web.login_fixture",  # 全局导入 Web 登录夹具
    "fixtures.app.app_fixture",  # 全局导入 APP 夹具
]
