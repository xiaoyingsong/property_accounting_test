import pytest
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, GLOBAL_TIMEOUT


# 第一步：定义浏览器级Fixture（会话级，只启动一次浏览器）
@pytest.fixture(scope="session")
def playwright_browser():
    with sync_playwright() as p:
        # 强制显示浏览器，延迟操作（调试必选）
        browser = p.chromium.launch(headless=False, slow_mo=500)
        yield browser  # 传递浏览器对象
        browser.close()

# 第二步：定义页面级Fixture（用例级，每个用例新建页面）
@pytest.fixture(scope="function")
def playwright_page(playwright_browser):
    context = playwright_browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    # ========== 新增：打印关键信息 + 捕获跳转异常 ==========
    # 1. 打印TEST_URL原始值
    print(f"\n[DEBUG] TEST_URL 配置值: {BASE_URL}")
    # 2. 拼接登录URL并打印
    login_url = f"{BASE_URL}/login"
    print(f"[DEBUG] 拼接后的登录URL: {login_url}")
    # 3. 检查URL格式
    print(f"[DEBUG] URL是否为空: {login_url is None or login_url == ''}")
    print(f"[DEBUG] URL是否有重复斜杠: {'//' in login_url}")

    try:
        # 页面可能有慢资源，使用更稳妥的文档就绪判定，避免 load 卡住
        response = page.goto(login_url, timeout=60000, wait_until="domcontentloaded")
        # 打印跳转响应结果
        if response:
            print(f"[INFO] goto响应状态码: {response.status}")
            print(f"[INFO] 跳转后实际URL: {page.url}")
        else:
            print("[ERROR] goto返回None，跳转失败")
    except Exception as e:
        print(f"\n[ERROR] page.goto 执行失败，原因: {str(e)}")
        # 抛出异常，让pytest显示（方便定位）
        raise

    yield page
    page.close()
    context.close()