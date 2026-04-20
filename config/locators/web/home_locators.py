# config/locators/web/home_locators.py
# 首页元素定位器（左侧导航）
HOME_LOCATORS = {
    # 项目设置中心菜单（文本定位）
    "project_setting_menu": ("get_by_text", "项目设置中心", {"exact": True, "timeout": 10000}),
    # 房屋单元子菜单（文本定位）
    "housing_unit_sub_menu": ("get_by_text", "房屋单元", {"exact": True, "timeout": 10000}),
    # 用户头像按钮（角色定位）
    "user_avatar_btn": ("get_by_role", "button", {"name": "用户头像", "timeout": 10000}),
    # 退出登录菜单项（角色定位）
    "logout_menu_item": ("get_by_role", "menuitem", {"name": "退出登录", "timeout": 10000}),
}
