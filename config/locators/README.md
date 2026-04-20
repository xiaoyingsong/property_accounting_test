# Locators 目录说明

本目录按端类型拆分定位器配置，避免混放导致维护困难。

## 目录结构

- `app/`: 存放 App 端定位器配置（Appium/Selenium）
- `web/`: 存放 Web 端定位器配置（Playwright）

示例：

- `config/locators/app/login_locators.py`
- `config/locators/web/home_locators.py`
- `config/locators/web/housing_unit_list_locators.py`
- `config/locators/web/housing_unit_form_locators.py`

## 约定规范

- 一个页面对应一个定位器配置文件（如 `xxx_locators.py`）
- 页面对象（`pages/...`）只负责业务动作与断言，不在页面类中硬编码大量定位表达式
- 新增定位器时，优先放入对应端目录（`app/` 或 `web/`）
- 禁止在 `config/locators` 根目录新增端无关定位器文件

## 引用方式

App 页面示例：

```python
from config.locators.app.login_locators import APP_LOGIN_LOCATORS
```

Web 页面示例：

```python
from config.locators.web.home_locators import HOME_LOCATORS
```

## 变更建议

- 定位器变更优先改配置，不直接改测试用例
- 变更后至少执行一次对应端用例收集或冒烟，确保导入与运行链路正常

