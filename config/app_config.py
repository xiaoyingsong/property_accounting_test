import os
from dotenv import load_dotenv

load_dotenv()

# ====================== APP 自动化核心配置 ======================
APPIUM_HOST = "127.0.0.1"
APPIUM_PORT = 4723

# MuMu 模拟器固定配置
DEVICE_NAME = "127.0.0.1:5557"
APP_PACKAGE = "com.cspeed.sevenlink"
APP_ACTIVITY = "com.cspeed.sevenlink.ui.activity.SplashActivity"

# 驱动配置
IMPLICITLY_WAIT = 10
NO_RESET = False  # 每次重启APP，避免缓存问题

# Appium 启动参数（适配 MuMu）
DESIRED_CAPS = {
    "platformName": "Android",
    "deviceName": DEVICE_NAME,
    "appPackage": APP_PACKAGE,
    "appActivity": APP_ACTIVITY,
    "automationName": "UiAutomator2",
    "noReset": NO_RESET,
    "adbExecTimeout": 80000,
    "uiautomator2ServerLaunchTimeout": 80000,
    "unicodeKeyboard": True,
    "resetKeyboard": True
}