# conftest.py 测试失败自动截图
import pytest
import allure
from playwright.sync_api import Page
from utils.log_utils import logger

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
        # 尝试从用例参数中获取 page 对象
        try:
            page: Page = item.funcargs["login_success_page"]  # 对应登录Fixture的参数名
            # 截图并附加到 Allure 报告
            screenshot = page.screenshot(full_page=True)  # 全屏截图
            allure.attach(
                screenshot,
                name=f"失败截图-{item.nodeid.split('::')[-1]}",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"✅ 失败截图已附加到 Allure 报告：{item.nodeid}")
        except Exception as e:
            logger.error(f"❌ 失败截图失败：{str(e)}")
            allure.attach(f"截图失败：{str(e)}", name="截图异常", attachment_type=allure.attachment_type.TEXT)

# pytest_plugins = [
#     "fixtures.test_app.app_fixture"  # 全局导入 APP 夹具
# ]