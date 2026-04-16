import os
from dotenv import load_dotenv
from config import get_env_config # 复用原有环境加载
load_dotenv(dotenv_path=get_env_config, override=True)

# ====================== APP 自动化核心配置 ======================
# Appium 服务地址
APPIUM_HOST = os.getenv("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = os.getenv("APPIUM_PORT", "4723")

# 安卓设备配置（必填）
DEVICE_NAME = os.getenv("DEVICE_NAME", "emulator-5554")
APP_PACKAGE = os.getenv("APP_PACKAGE")  # APP 包名
APP_ACTIVITY = os.getenv("APP_ACTIVITY")  # APP 启动页面

# 驱动配置
IMPLICITLY_WAIT = int(os.getenv("IMPLICITLY_WAIT", 10))  # 隐式等待
NO_RESET = os.getenv("NO_RESET", "True").lower() == "true"  # 不重置 APP

# Appium 启动参数（Desired Capabilities）
DESIRED_CAPS = {
    "platformName": "Android",
    "deviceName": DEVICE_NAME,
    "appPackage": APP_PACKAGE,
    "appActivity": APP_ACTIVITY,
    "noReset": NO_RESET,
    "automationName": "UiAutomator2",
    "unicodeKeyboard": True,
    "resetKeyboard": True
}