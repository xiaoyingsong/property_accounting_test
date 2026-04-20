import os
import sys

# 兼容直接执行该文件时的导入路径（python test_xxx.py）
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from pages.app.login_app_page import LoginAppPage
import time


class TestAppLogin:
    def test_app_login_success(self, app_driver):
        """
        用例名称：7Link APP-登录成功
        流程：打开APP → 输入账号密码 → 点击登录 → 断言成功
        """
        # 1. 初始化登录页对象
        login_page = LoginAppPage(app_driver)
        print("APP启动成功，等待登录页加载...")
        time.sleep(3)

        # 2. 执行登录（替换成你的测试账号）
        login_page.login(username="1001@tianmi.me", password="Song123456")
        print("账号密码输入完成，点击登录...")
        time.sleep(3)

        # 3. 断言登录成功
        assert login_page.is_login_success() is True, "登录失败"
        print("登录成功，用例执行通过")
