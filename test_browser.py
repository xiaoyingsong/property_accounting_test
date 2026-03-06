from playwright.sync_api import sync_playwright

# 这段代码只做一件事：打开浏览器 → 打开百度 → 停住
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 看得见的浏览器
    page = browser.new_page()
    page.goto("https://www.baidu.com")

    print("✅ 浏览器打开成功！")
    page.pause()  # 让浏览器停住，不会立刻关掉

    browser.close()