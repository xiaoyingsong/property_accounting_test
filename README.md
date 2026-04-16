# 自动化测试项目（pytest + playwright + allure）
该项目基于 `pytest` 测试框架、`playwright` 浏览器自动化工具、`allure` 测试报告工具，采用**页面对象模式（PO）** 实现Web端自动化测试，支持多浏览器运行、用例分层管理、测试报告可视化、失败重跑/并行执行等核心能力。

## 一、环境准备
### 1. 基础环境
- Python 3.8+（推荐3.9/3.10，与playwright兼容性最佳）
- 操作系统：Windows/macOS/Linux（playwright全平台支持）
- 网络环境：可正常访问被测Web站点

### 2. 浏览器依赖（playwright自动安装）
playwright内置Chrome、Firefox、WebKit（Safari内核）支持，无需手动安装浏览器，执行以下命令自动下载二进制文件：
```bash
# 安装所有浏览器（chromium/firefox/webkit）
playwright install

# 仅安装指定浏览器（如仅chromium）
playwright install chromium
```

## 二、安装项目依赖
1. 项目根目录创建 `requirements.txt`，内容如下：
```txt
pytest>=7.0.0
playwright>=1.30.0
pytest-playwright>=0.3.0
allure-pytest>=2.13.2
python-dotenv>=1.0.0  # 环境变量管理
pytest-rerunfailures>=11.1.1  # 失败重跑
pytest-xdist>=3.3.1    # 并行执行
```

2. 执行安装命令：
```bash
pip install -r requirements.txt
```

## 三、项目目录结构
```
auto-test-project/
├── config/                # 配置文件目录
│   ├── setting.py         # 全局配置（URL、浏览器、超时时间等）
│   └── .env               # 环境变量（敏感信息：账号、密码等）
├── fixtures/              # Pytest夹具目录（通用前置/后置逻辑）
│   ├── conftest.py        # Pytest核心夹具（全局生效）
│   ├── browser_fixture.py # 浏览器/页面专属夹具（可选）
│   └── common_fixture.py  # 业务通用夹具（可选）
├── logs/                  # 日志目录（自动生成）
│   └── test_run.log       # 测试执行日志
├── pages/                 # 页面对象(PO)目录（按业务模块分层）
│   ├── base_page.py       # 页面基类（封装通用操作）
│   ├── login_page.py      # 登录页元素/操作封装
│   └── home_page.py       # 首页元素/操作封装
├── test_cases/            # 测试用例目录（按业务模块划分）
│   ├── test_login.py      # 登录功能用例
│   └── test_home.py       # 首页功能用例
├── utils/                 # 工具类目录
│   ├── logger.py          # 日志封装
│   ├── common_utils.py    # 通用方法（截图、数据处理等）
│   └── screenshot/        # 截图目录（自动生成）
├── requirements.txt       # 项目依赖清单
├── allure-results/        # Allure原始报告（自动生成）
└── allure-report/         # Allure静态报告（生成后可见）
```

### 目录核心作用说明
| 目录        | 核心作用                                                                 |
|-------------|--------------------------------------------------------------------------|
| `config`    | 集中管理配置，避免硬编码；`.env`存放敏感信息，`setting.py`读取并暴露配置 |
| `fixtures`  | 封装Pytest夹具，实现代码复用；`conftest.py`为Pytest默认加载的夹具文件     |
| `logs`      | 存储测试执行日志，便于问题排查                                           |
| `pages`     | 基于PO模式封装页面元素和操作，降低用例与页面耦合                         |
| `test_cases`| 编写测试用例，仅关注业务逻辑，调用pages层封装的方法                      |
| `utils`     | 封装通用工具方法（日志、截图、数据处理），提升代码复用性                 |

## 四、核心模块实现
### 1. 配置模块（config/）
#### config/setting.py（全局配置读取）
```python
import os
from dotenv import load_dotenv

# 加载.env环境变量（优先读取config目录下的.env）
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# 测试环境基础配置
TEST_URL = os.getenv("TEST_URL", "https://test.example.com")
BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")  # 浏览器类型：chromium/firefox/webkit
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "True").lower() == "true"  # 无头模式
SLOW_MO = int(os.getenv("SLOW_MO", 500))  # 慢动作延迟（毫秒，便于调试）
LOCATOR_TIMEOUT = int(os.getenv("LOCATOR_TIMEOUT", 10000))  # 元素定位超时

# 测试账号（从.env读取，避免硬编码）
TEST_USER = os.getenv("TEST_USER")
TEST_PWD = os.getenv("TEST_PWD")
```

#### config/.env（环境变量文件，需加入.gitignore）
```env
# 测试环境地址
TEST_URL=https://test.example.com
# 浏览器配置
BROWSER_TYPE=chromium
HEADLESS_MODE=False
SLOW_MO=300
LOCATOR_TIMEOUT=10000
# 测试账号（敏感信息）
TEST_USER=auto_test_01
TEST_PWD=Test@123456
```

### 2. 页面对象模块（pages/）
#### pages/base_page.py（页面基类，封装通用操作）
```python
from playwright.sync_api import Page, expect
from config.setting import LOCATOR_TIMEOUT

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = LOCATOR_TIMEOUT

    # 通用：页面跳转
    def goto(self, url: str):
        self.page.goto(url, timeout=self.timeout)

    # 通用：输入文本
    def input_text(self, locator: str, text: str):
        self.page.locator(locator).fill(text, timeout=self.timeout)

    # 通用：点击元素
    def click(self, locator: str):
        self.page.locator(locator).click(timeout=self.timeout)

    # 通用：断言URL
    def assert_url(self, expected_url: str):
        expect(self.page).to_have_url(expected_url, timeout=self.timeout)

    # 通用：断言文本
    def assert_text(self, locator: str, expected_text: str):
        expect(self.page.locator(locator)).to_have_text(expected_text, timeout=self.timeout)
```

#### pages/login_page.py（登录页封装）
```python
from pages.base_page import BasePage
from config.setting import TEST_URL

class LoginPage(BasePage):
    # 元素定位器（统一管理，便于维护）
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    SUBMIT_BTN = "button[type='submit']"
    ERROR_TIPS = ".error-tips"

    # 页面URL
    LOGIN_URL = f"{TEST_URL}/login"

    def __init__(self, page):
        super().__init__(page)

    # 打开登录页
    def open(self):
        self.goto(self.LOGIN_URL)

    # 执行登录操作
    def login(self, username: str, password: str):
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    # 断言登录失败提示
    def assert_login_fail(self, tips: str):
        self.assert_text(self.ERROR_TIPS, tips)
```

#### pages/home_page.py（首页封装）
```python
from pages.base_page import BasePage
from config.setting import TEST_URL

class HomePage(BasePage):
    # 元素定位器
    USER_AVATAR = ".user-name"
    MENU_DASHBOARD = "#menu-dashboard"

    # 页面URL
    HOME_URL = f"{TEST_URL}/home"

    def __init__(self, page):
        super().__init__(page)

    # 断言成功进入首页
    def assert_in_home(self):
        self.assert_url(self.HOME_URL)

    # 断言用户名显示正确
    def assert_user_name(self, username: str):
        self.assert_text(self.USER_AVATAR, username)
```

### 3. 夹具模块（fixtures/）
#### fixtures/conftest.py（Pytest核心夹具，自动加载）
```python
import pytest
import logging
from playwright.sync_api import sync_playwright
from config.setting import BROWSER_TYPE, HEADLESS_MODE, SLOW_MO
from utils.logger import init_logger

# 初始化日志
init_logger()
logger = logging.getLogger(__name__)

# -------------------------- 全局夹具 --------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    """Playwright实例（会话级，所有用例共享）"""
    with sync_playwright() as p:
        logger.info("✅ Playwright实例已启动")
        yield p
        logger.info("❌ Playwright实例已销毁")

@pytest.fixture(scope="function")
def page(playwright_instance):
    """浏览器页面（用例级，每个用例独立）"""
    # 启动浏览器
    browser = getattr(playwright_instance, BROWSER_TYPE).launch(
        headless=HEADLESS_MODE,
        slow_mo=SLOW_MO
    )
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})  # 固定窗口大小
    logger.info(f"🔍 启动{BROWSER_TYPE}浏览器，无头模式：{HEADLESS_MODE}")

    yield page

    # 用例后置操作：失败截图 + 关闭资源
    if page.error:
        from utils.common_utils import take_screenshot
        take_screenshot(page, "error_case")
        logger.error(f"❌ 用例执行失败，已生成错误截图")
    context.close()
    browser.close()
    logger.info("🔌 浏览器页面已关闭")

# -------------------------- 业务夹具 --------------------------
@pytest.fixture(scope="function")
def login_page(page):
    """登录页对象（用例级）"""
    from pages.login_page import LoginPage
    return LoginPage(page)

@pytest.fixture(scope="function")
def home_page(page):
    """首页对象（用例级）"""
    from pages.home_page import HomePage
    return HomePage(page)
```

### 4. 工具模块（utils/）
#### utils/logger.py（日志封装）
```python
import logging
import os
from datetime import datetime

# 日志目录（自动创建）
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志文件名（按时间戳命名）
LOG_FILE = os.path.join(LOG_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def init_logger():
    """初始化日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # 控制台输出
            logging.FileHandler(LOG_FILE, encoding="utf-8")  # 文件输出
        ]
    )
```

#### utils/common_utils.py（通用工具）
```python
import os
from playwright.sync_api import Page

def take_screenshot(page: Page, case_name: str):
    """
    生成用例截图（全屏）
    :param page: 浏览器页面对象
    :param case_name: 用例名称（作为截图文件名前缀）
    """
    screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshot")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    file_name = f"{case_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot_path = os.path.join(screenshot_dir, file_name)
    page.screenshot(path=screenshot_path, full_page=True)
    return screenshot_path
```

## 五、测试用例编写（test_cases/）
### test_cases/test_login.py（登录功能用例）
```python
import pytest
from config.setting import TEST_USER, TEST_PWD

# 登录成功用例
@pytest.mark.login  # 用例标签，便于筛选执行
def test_login_success(login_page, home_page):
    """登录成功：验证跳转首页且用户名显示正确"""
    # 步骤1：打开登录页并执行登录
    login_page.open()
    login_page.login(TEST_USER, TEST_PWD)
    # 步骤2：断言结果
    home_page.assert_in_home()
    home_page.assert_user_name(TEST_USER)

# 登录失败用例（数据驱动）
@pytest.mark.login
@pytest.mark.parametrize("username, pwd, error_tips", [
    (TEST_USER, "WrongPass123", "密码错误，请重新输入"),
    (TEST_USER, "", "密码不能为空"),
    ("invalid_user", TEST_PWD, "账号不存在"),
])
def test_login_fail(login_page, username, pwd, error_tips):
    """登录失败：验证不同错误场景的提示文案"""
    login_page.open()
    login_page.login(username, pwd)
    login_page.assert_login_fail(error_tips)
```

### test_cases/test_home.py（首页功能用例）
```python
import pytest
from config.setting import TEST_USER, TEST_PWD

@pytest.mark.home
def test_home_menu_click(login_page, home_page):
    """首页功能：验证菜单点击跳转正确"""
    # 前置：登录
    login_page.open()
    login_page.login(TEST_USER, TEST_PWD)
    
    # 操作：点击仪表盘菜单
    home_page.click(home_page.MENU_DASHBOARD)
    # 断言：菜单激活状态
    home_page.assert_text("#dashboard-active", "仪表盘")
```

## 六、运行测试用例
### 1. 核心运行命令
```bash
# 运行所有用例（生成Allure原始报告）
pytest test_cases/ --alluredir=allure-results -v -s

# 仅运行指定标签的用例（如login标签）
pytest test_cases/ -m login --alluredir=allure-results -v

# 并行执行用例（按CPU核心数自动分配进程）
pytest test_cases/ -n auto --alluredir=allure-results

# 失败重跑（失败用例重跑2次）
pytest test_cases/ --reruns=2 --alluredir=allure-results

# 仅运行上一次失败的用例
pytest test_cases/ --lf --alluredir=allure-results

# 临时切换浏览器运行（覆盖.env配置）
BROWSER_TYPE=firefox pytest test_cases/ --alluredir=allure-results
```

### 2. 常用参数说明
| 参数          | 说明                                                                 |
|---------------|----------------------------------------------------------------------|
| `-v`          | 详细输出用例执行结果（显示用例名称、执行状态）                       |
| `-s`          | 显示代码中的print/logging日志（默认屏蔽）                            |
| `-m`          | 按标签筛选用例（如`-m login`仅运行@pytest.mark.login的用例）         |
| `-n auto`     | 并行执行用例，提升执行效率                                           |
| `--reruns`    | 失败用例重跑次数（如`--reruns=2`）                                  |
| `--lf`        | 仅运行上一次失败的用例（Last Failed）                                |
| `--alluredir` | 指定Allure原始报告输出目录（必须配置才能生成Allure报告）             |

## 七、生成Allure测试报告
### 1. 安装Allure命令行工具
- **Windows**：下载Allure压缩包（https://github.com/allure-framework/allure2/releases），解压后将`bin`目录添加到系统环境变量；
- **macOS**：`brew install allure`；
- **Linux**：`sudo apt-get install allure`。

### 2. 生成&查看报告
```bash
# 生成静态Allure报告（输出到allure-report目录）
allure generate allure-results -o allure-report --clean

# 启动本地服务，查看交互式报告（自动打开浏览器）
allure serve allure-results

# 直接查看静态报告（打开allure-report/index.html）
```

### 3. 报告核心能力
- 可视化展示用例通过率、执行时长、失败原因；
- 支持按标签/模块/执行状态筛选用例；
- 失败用例自动关联截图、日志、堆栈信息；
- 可导出HTML/PDF格式报告，便于分享。

## 八、常见问题与解决方案
### 1. Playwright启动浏览器失败
- 原因：浏览器二进制文件缺失、Python版本不兼容、权限不足；
- 解决：
  ```bash
  # 强制重新安装浏览器二进制文件
  playwright install --force
  # 验证Python版本（需3.8+）
  python --version
  ```

### 2. Allure报告无法生成
- 原因：Allure未安装/环境变量未配置、`allure-results`目录为空；
- 解决：
  - 验证Allure安装：`allure --version`；
  - 确保运行用例时添加`--alluredir=allure-results`参数。

### 3. 元素定位超时/失败
- 原因：选择器错误、页面加载慢、元素未渲染；
- 解决：
  - 用`playwright codegen 测试URL`生成精准选择器；
  - 延长`config/setting.py`中的`LOCATOR_TIMEOUT`；
  - 优先使用`expect`断言（自动等待元素渲染），避免`time.sleep()`。

## 九、最佳实践与扩展
### 1. 代码规范
- 用例保持“原子性”：一个用例仅验证一个功能点；
- PO模式：页面操作封装到`pages/`，用例仅关注业务逻辑；
- 敏感信息：所有账号/密码/密钥放在`.env`，且`.env`加入`.gitignore`；
- 日志/截图：关键操作加日志，失败用例自动截图，便于问题定位。

### 2. CI/CD集成（Jenkins示例）
```bash
# Jenkins流水线核心步骤
pipeline {
    agent any
    stages {
        stage('安装依赖') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install'
            }
        }
        stage('执行用例') {
            steps {
                sh 'pytest test_cases/ -n auto --reruns=2 --alluredir=allure-results'
            }
        }
        stage('生成报告') {
            steps {
                sh 'allure generate allure-results -o allure-report --clean'
            }
            post {
                always {
                    allure includeProperties: false, jdk: '', report: 'allure-report'
                }
            }
        }
    }
}
```

### 3. 扩展能力
- **多环境切换**：新增`.env.test`/`.env.prod`，通过加载不同配置文件切换环境；
- **告警推送**：用例执行完成后，通过钉钉/邮件推送测试结果；
- **数据驱动增强**：读取Excel/CSV文件，实现大规模测试数据管理；
- **接口联动**：结合`requests`库，实现“接口+UI”一体化测试。

## 十、注意事项
1. 定期更新playwright版本，适配最新浏览器特性；
2. 避免用例之间的依赖（如“登录用例”不依赖“注册用例”执行）；
3. 测试环境不稳定时，可适当延长超时时间或增加失败重跑次数；
4. 提交代码时，忽略`logs/`、`allure-results/`、`utils/screenshot/`等临时目录。