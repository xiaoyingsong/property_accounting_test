# config/locators/web/housing_unit_form_locators.py
# 新增房屋单元表单元素定位器
HOUSING_UNIT_FORM_LOCATORS = {
    # 表单标题（角色定位）
    "form_title": ("get_by_role", "heading", {"name": "新增房屋单元", "timeout": 10000}),
    # 楼栋下拉框（CSS定位）
    "building_select": ("locator", "label:has-text('楼栋') + .el-select", {"timeout": 10000}),
    # 单元号输入框（占位符定位）
    "unit_input": ("get_by_placeholder", "请输入单元号", {"timeout": 10000}),
    # 房号输入框（占位符定位）
    "room_input": ("get_by_placeholder", "请输入房号", {"timeout": 10000}),
    # 建筑面积输入框（占位符定位）
    "built_area_input": ("get_by_placeholder", "请输入建筑面积", {"timeout": 10000}),
    # 保存按钮（角色定位）
    "save_button": ("get_by_role", "button", {"name": "保存", "timeout": 10000}),
    # 提交成功提示（文本定位）
    "success_msg": ("get_by_text", "提交成功", {"timeout": 5000}),
}
