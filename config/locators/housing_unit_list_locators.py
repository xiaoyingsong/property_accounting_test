# utils/locator_parser.py
import logging
from playwright.sync_api import Page

# 初始化日志
logger = logging.getLogger(__name__)

def parse_locator(page: Page, locator_config: tuple):
    """
    通用定位器解析方法：将配置转换为Playwright Locator对象
    :param page: Playwright的Page对象
    :param locator_config: 定位器配置，格式=(定位方法, 核心参数, 关键字参数字典)
    :return: Playwright Locator对象
    """
    try:
        locator_method, main_param, kwargs = locator_config
        # 按定位方法解析，严格匹配Playwright API
        if locator_method == "get_by_text":
            return page.get_by_text(main_param, **kwargs)
        elif locator_method == "get_by_role":
            return page.get_by_role(main_param, **kwargs)
        elif locator_method == "get_by_placeholder":
            return page.get_by_placeholder(main_param, **kwargs)
        elif locator_method == "locator":
            return page.locator(main_param, **kwargs)
        else:
            raise ValueError(f"不支持的定位方法：{locator_method}")
    except Exception as e:
        logger.error(f"解析定位器失败！配置：{locator_config}，错误：{str(e)}")
        raise  # 抛出异常，便于定位问题

def parse_dynamic_locator(page: Page, base_config: tuple, replace_map: dict):
    """
    解析带占位符的动态定位器（如：{"room_row": ("get_by_role", "row", {"name": "{room_no}"})}）
    :param replace_map: 占位符替换字典，如{"room_no": "A-01-01"}
    """
    locator_method, main_param, kwargs = base_config
    # 替换主参数中的占位符（如{room_no} → A-01-01）
    main_param = main_param.format(**replace_map)
    # 重新解析
    return parse_locator(page, (locator_method, main_param, kwargs))