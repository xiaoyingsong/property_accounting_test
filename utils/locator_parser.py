# utils/locator_parser.py（最终兼容版）
import logging
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


def parse_locator(page: Page, locator_config: tuple):
    """
    兼容所有Playwright版本的定位器解析方法
    移除with_timeout，超时在元素操作/断言阶段控制
    locator_config格式：(定位方法, 核心参数, 参数字典)
    参数字典中仅保留定位方法支持的参数（如exact、name等），timeout仅作为标记备用
    """
    try:
        locator_method, main_param, kwargs = locator_config

        # 1. 移除timeout（仅保留定位方法支持的参数）
        kwargs.pop("timeout", None)  # 删掉timeout，避免传给定位方法

        # 2. 创建定位器（仅传定位方法支持的参数）
        if locator_method == "get_by_text":
            locator = page.get_by_text(main_param, **kwargs)
        elif locator_method == "get_by_role":
            locator = page.get_by_role(main_param, **kwargs)
        elif locator_method == "get_by_placeholder":
            locator = page.get_by_placeholder(main_param, **kwargs)
        elif locator_method == "locator":
            locator = page.locator(main_param, **kwargs)
        else:
            raise ValueError(f"不支持的定位方法：{locator_method}")

        return locator
    except Exception as e:
        logger.error(f"解析定位器失败！配置：{locator_config}，错误：{str(e)}")
        raise


def parse_dynamic_locator(page: Page, base_config: tuple, replace_map: dict):
    """解析带占位符的动态定位器（逻辑不变）"""
    locator_method, main_param, kwargs = base_config
    main_param = main_param.format(**replace_map)
    return parse_locator(page, (locator_method, main_param, kwargs))