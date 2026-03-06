# config/env_config.py
# 环境枚举（避免手写字符串出错）
ENV_TYPES = {
    "TEST": "test",    # 测试环境
    "PROD": "prod",    # 生产环境
    "UAT": "uat"       # 验收环境
}

# 默认环境（可通过命令行参数覆盖）
CURRENT_ENV = ENV_TYPES["TEST"]

# 各环境配置
ENV_CONFIG = {
    "test": {
        "BASE_URL": "http://tenant.7link.local",
        "TIMEOUT": 10000,  # 通用超时时间（毫秒）
        "HEADLESS": False  # 是否无头模式
    },
    "prod": {
        "BASE_URL": "https://prod-property-system.com",
        "TIMEOUT": 10000,
        "HEADLESS": True
    },
    "uat": {
        "BASE_URL": "https://uat-property-system.com",
        "TIMEOUT": 10000,
        "HEADLESS": False
    }
}

# 快捷获取当前环境配置
def get_env_config():
    return ENV_CONFIG[CURRENT_ENV]

# 快捷获取BASE_URL
BASE_URL = get_env_config()["BASE_URL"]
# 快捷获取通用超时
GLOBAL_TIMEOUT = get_env_config()["TIMEOUT"]