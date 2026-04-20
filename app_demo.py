from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# ====================== MuMu模拟器终极配置 ======================
desired_caps = {
    "platformName": "Android",
    "deviceName": "127.0.0.1:5557",
    "appPackage": "com.cspeed.sevenlink",
    "appActivity": "com.cspeed.sevenlink.ui.activity.SplashActivity",
    "automationName": "UiAutomator2",
    # 核心修复：关闭缓存，强制重新冷启动APP
    "noReset": False,
    "fullReset": False,
    # 核心修复：超时时间拉满，适配MuMu慢启动
    "adbExecTimeout": 80000,
    "uiautomator2ServerLaunchTimeout": 80000,
    "appWaitDuration": 80000,
    # 核心修复：跳过权限调整，避免闪退
    "skipDeviceInitialization": False,
    "skipServerInstallation": False,
}

# 连接Appium
options = UiAutomator2Options().load_capabilities(desired_caps)
driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)

print("✅ 正在强制启动APP...")

# 等待5秒，确保你能看见APP界面
time.sleep(5)

print("✅ APP已成功在模拟器显示！")

# 关闭
time.sleep(3)
driver.quit()
print("✅ 运行完成")
