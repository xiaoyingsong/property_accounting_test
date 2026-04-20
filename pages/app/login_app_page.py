from pages.app.base_app_page import BaseAppPage
from config.locators.app.login_locators import APP_LOGIN_LOCATORS
import time


class LoginAppPage(BaseAppPage):
    USERNAME_INPUT = APP_LOGIN_LOCATORS["username_input"]
    PASSWORD_INPUT = APP_LOGIN_LOCATORS["password_input"]
    LOGIN_BTN = APP_LOGIN_LOCATORS["login_button"]
    AGREE_BTN = APP_LOGIN_LOCATORS["agree_button"]
    HOME_SUCCESS_TEXT = APP_LOGIN_LOCATORS["home_success_text"]

    def login(self, username: str, password: str):
        # 强制等待页面加载（MuMu必加）
        time.sleep(3)

        # 输入账号
        self.input(self.USERNAME_INPUT, username)
        time.sleep(1)

        # 输入密码
        self.input(self.PASSWORD_INPUT, password)
        time.sleep(1)

        # 点击登录
        self.click(self.LOGIN_BTN)
        time.sleep(1)

        # 点击同意并继续
        self.click(self.AGREE_BTN)

    def is_login_success(self):
        """断言：登录是否成功"""
        return self.get_text(self.HOME_SUCCESS_TEXT) == "首页"
