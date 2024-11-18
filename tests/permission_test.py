# 用户权限数据
from utils.Permission import Permission

permissions_data = {
    'comic': [Permission.READ,Permission.ADD,Permission.DELETE,Permission.MODIFY,Permission.SPECIAL],  # 漫画分类有READ和ADD权限
    'article': [Permission.READ,Permission.ADD,Permission.DELETE,Permission.MODIFY,Permission.SPECIAL],  # 文章分类有READ和MODIFY权限
    'magazine': [Permission.READ,Permission.ADD,Permission.DELETE,Permission.MODIFY,Permission.SPECIAL],  # 杂志分类有READ和DELETE权限
    'user': [Permission.READ,Permission.ADD,Permission.DELETE,Permission.MODIFY,Permission.SPECIAL],  # 用户分类有ADD和MODIFY权限
    'settings': [Permission.READ,Permission.ADD,Permission.DELETE,Permission.MODIFY,Permission.SPECIAL]  # 设置分类有SPECIAL权限
}
# 生成权限字符串
permission_string = Permission.generate_permission_string(permissions_data)
print("生成的权限字符串:", permission_string)  # 输出权限字符串，例如："0303120100"

# 解析权限字符串
parsed_permissions = Permission.parse_permission_string(permission_string)
print("解析后的权限:", parsed_permissions)

# 检查某个分类的权限
result = Permission.has_permission(3131313131, 'user', Permission.ADD)
print("用户是否有漫画分类的ADD权限:", result)  # True

result = Permission.has_permission(permission_string, 'article', Permission.DELETE)
print("用户是否有文章分类的DELETE权限:", result)  # False
