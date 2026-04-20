import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

# 你的APP配置（已适配MuMu模拟器）
DESIRED_CAPS = {
    "platformName": "Android",
    "deviceName": "127.0.0.1:5557",
    "appPackage": "com.cspeed.sevenlink",
    "appActivity": "com.cspeed.sevenlink.ui.activity.SplashActivity",
    "automationName": "UiAutomator2",
    # 与 app_demo.py 对齐：使用冷启动，避免复用历史状态导致页面不一致
    "noReset": False,
    "fullReset": False,
    "adbExecTimeout": 80000,
    "uiautomator2ServerLaunchTimeout": 80000,
    "appWaitDuration": 80000,
    "skipDeviceInitialization": False,
    "skipServerInstallation": False,
}


# 启动/关闭 APP 驱动
@pytest.fixture(scope="function")
def app_driver():
    # 连接Appium，自动打开APP
    options = UiAutomator2Options().load_capabilities(DESIRED_CAPS)
    driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)
    yield driver
    # 用例执行完，关闭APP
    driver.quit()
