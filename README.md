# 7Link 自动化测试框架（测试人员使用版）

本项目是 UI 自动化测试框架，包含两条链路：

- **Web**：`pytest + playwright + allure`
- **App**：`pytest + appium + allure`

框架采用 **PO（Page Object）模式**：用例只写业务步骤；页面操作在 `pages/`；元素定位在 `config/locators/`；环境前后置在 `fixtures/`。

---

## 快速开始

### 1）安装依赖

在项目根目录执行：

```bash
pip install -r requirements.txt
```

### 2）Web：安装 Playwright 浏览器驱动

```bash
playwright install
```

### 3）App：准备 Appium + 设备

- **Appium Server**：需启动并监听 `http://127.0.0.1:4723`
- **模拟器/真机**：当前配置示例为 MuMu（`deviceName=127.0.0.1:5557`）

> App 启动能力参数在 `fixtures/app/app_fixture.py` 中维护。

---

## 运行用例（推荐命令）

说明：项目已在 `pytest.ini` 配置默认参数：

- `-s`：显示 print/log 输出
- `--alluredir=./test_cases/allure-results`：Allure 原始数据输出目录
- `--clean-alluredir`：每次执行前清空 Allure 输出目录

所以一般直接执行 pytest 即可。

### Web：运行用例文件

```bash
python -m pytest -s -v test_cases/test_web/test_base.py
```

### App：运行用例文件

```bash
python -m pytest -s -v test_cases/test_app/test_app_login.py
```

### 只跑某一条用例

```bash
python -m pytest -s -v test_cases/test_app/test_app_login.py::TestAppLogin::test_app_login_success
```

---

## Allure 报告与失败截图

### 1）Allure 原始数据目录

- `test_cases/allure-results`

### 2）失败自动截图

项目在 `conftest.py` 中实现失败自动截图：

- **Web**：对 Playwright `Page` 截图
- **App**：对 Appium `driver` 截图（`get_screenshot_as_png`）
- 截图会 **落盘到 `test_cases/allure-results`**，同时 **attach 到 Allure**

### 3）查看 Allure 报告

本机安装 Allure 命令行后执行：

```bash
allure serve test_cases/allure-results
```

---

## 项目目录说明（测试人员重点）

```text
config/
  config.py                 # Web 配置（BASE_URL、GLOBAL_TIMEOUT 等）
  login_data.py             # Web 登录账号数据（DEFAULT_LOGIN_DATA）
  locators/                 # 定位器配置（已按 app/web 分层）
    app/                    # App 端定位器（Appium/Selenium）
    web/                    # Web 端定位器（Playwright）

fixtures/
  app/app_fixture.py        # App：启动/关闭 driver（fixture: app_driver）
  web/browser_fixture.py    # Web：启动浏览器/创建 Page（fixture: playwright_page）
  web/login_fixture.py      # Web：登录并返回已登录 Page（fixture: login_success_page）

pages/
  app/                      # App：页面对象（PO）
  web/                      # Web：页面对象（PO）

test_cases/
  test_app/                 # App 用例
  test_web/                 # Web 用例
  allure-results/           # Allure 原始数据 + 失败截图（自动生成）

conftest.py                 # pytest 全局钩子：失败截图 + 注册 fixtures 插件
pytest.ini                  # pytest 默认参数（含 alluredir）
requirements.txt            # 依赖清单
```

---

## PO 模式四层关系（必须掌握）

**test_cases（写业务步骤）**
→ 使用 **fixtures（拿到已准备好的 page/driver）**
→ 调用 **pages（页面对象方法）**
→ pages 内部使用 **config/locators（定位器配置）**

---

## 配置说明（常用）

### Web 基础配置

- `config/config.py` 中维护：
  - `BASE_URL`：被测系统地址
  - `GLOBAL_TIMEOUT`：Web 全局等待超时（毫秒）

### Web 登录账号

- `config/login_data.py` 中维护 `DEFAULT_LOGIN_DATA`

---

## 新增用例（推荐流程）

### 新增 Web 用例

1. 在 `test_cases/test_web/` 新建 `test_xxx.py`
2. 用例参数优先使用 `login_success_page`（已登录的 Playwright `Page`）
3. 业务步骤调用 `pages/web` 的页面对象方法
4. 若元素定位有变更：优先改 `config/locators/web/`

### 新增 App 用例

1. 在 `test_cases/test_app/` 新建 `test_xxx.py`
2. 用例参数使用 `app_driver`（Appium driver）
3. 业务步骤调用 `pages/app` 的页面对象方法
4. 若元素定位有变更：优先改 `config/locators/app/`

---

## 常见问题（项目内高频）

### 1）Web 无法打开/元素定位超时

- 确认已执行 `playwright install`
- 确认 `config/config.py` 中 `BASE_URL` 正确

### 2）App 启动失败/定位不稳定

- 确认 Appium Server 已启动：`127.0.0.1:4723`
- 确认设备连接信息（MuMu 端口等）与 `fixtures/app/app_fixture.py` 一致

