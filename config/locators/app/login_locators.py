# config/locators/app/login_locators.py
# APP 登录页元素定位器
from selenium.webdriver.common.by import By


APP_LOGIN_LOCATORS = {
    # 账号输入框
    "username_input": (
        By.XPATH,
        "//android.widget.ScrollView/android.view.View[5]/android.view.View[1]/android.widget.EditText",
    ),
    # 密码输入框
    "password_input": (
        By.XPATH,
        "//android.widget.ScrollView/android.view.View[5]/android.view.View[2]/android.widget.EditText",
    ),
    # 登录按钮
    "login_button": (
        By.XPATH,
        "//android.widget.ScrollView/android.view.View[5]/android.view.View[5]/android.view.View/android.widget.Button",
    ),
    # 同意/继续按钮（弹窗）
    "agree_button": (By.CLASS_NAME, "android.widget.Button"),
    # 首页成功标识
    "home_success_text": (
        By.XPATH,
        "//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]",
    ),
}
