# config/login_data.py
# 登录数据（按角色分组）
LOGIN_DATA = {
    "admin": {  # 管理员账号（有新增权限）
        "email": "songxiaoying101@gmail.com",
        "password": "Song123456.",
        "remember_me": True
    },
}

# 快捷获取默认登录账号（管理员）
DEFAULT_LOGIN_DATA = LOGIN_DATA["admin"]