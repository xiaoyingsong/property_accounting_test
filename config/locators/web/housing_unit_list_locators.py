# config/locators/web/housing_unit_list_locators.py
from utils.locator_parser import parse_dynamic_locator


HOUSING_UNIT_LIST_LOCATORS = {
    "add_button": ("get_by_role", "button", {"name": "新增", "timeout": 10000}),
    "page_title": ("get_by_role", "heading", {"name": "房屋单元管理", "timeout": 10000}),
    "loading_mask": ("locator", ".el-loading-mask", {"timeout": 5000}),
    # 动态行（示例保留）
    "room_row": ("get_by_role", "row", {"name": "{room_no}", "timeout": 10000}),
}


def get_room_row(page, room_no: str):
    return parse_dynamic_locator(page, HOUSING_UNIT_LIST_LOCATORS["room_row"], {"room_no": room_no})
