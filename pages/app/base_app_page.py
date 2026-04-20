from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BaseAppPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)  # 超长等待，适配MuMu

    # 点击元素
    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        time.sleep(0.5)

    # 输入文本
    def input(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)
        time.sleep(0.5)

    # 获取页面文本（用于断言）
    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text