class Permission:
    # 定义每个权限的位值
    READ = 1  # 00001
    ADD = 2  # 00010
    DELETE = 4  # 00100
    MODIFY = 8  # 01000
    SPECIAL = 16  # 10000

    # 分类列表
    CATEGORIES = ['comic', 'article', 'magazine', 'user', 'settings']

    # 每个分类的权限映射
    CATEGORY_PERMISSIONS = {
        'comic': [READ, ADD, DELETE, MODIFY, SPECIAL],
        'article': [READ, ADD, DELETE, MODIFY, SPECIAL],
        'magazine': [READ, ADD, DELETE, MODIFY, SPECIAL],
        'user': [READ, ADD, DELETE, MODIFY, SPECIAL],
        'settings': [READ, ADD, DELETE, MODIFY, SPECIAL]
    }

    @classmethod
    def generate_permission_string(cls, permissions):
        """根据分类权限生成一个整数表示的权限值"""
        permission_value = 0
        for category in cls.CATEGORIES:
            category_permissions = cls.CATEGORY_PERMISSIONS.get(category)
            category_value = 0
            for perm in category_permissions:
                if perm in permissions.get(category, []):
                    category_value |= perm  # 将权限合并到该分类
            permission_value |= category_value << (cls.CATEGORIES.index(category) * 5)  # 每个分类占5位

        return permission_value

    @classmethod
    def parse_permission_string(cls, permission_value):
        """解析权限整数，返回每个分类的权限列表"""
        permissions = {}
        for index, category in enumerate(cls.CATEGORIES):
            category_value = (permission_value >> (index * 5)) & 0x1F  # 右移并取5位
            permissions[category] = cls.get_permissions_from_value(category_value)

        return permissions

    @classmethod
    def get_permissions_from_value(cls, value):
        """根据权限值获取对应的权限列表"""
        permissions = []
        if value & cls.READ:
            permissions.append(cls.READ)
        if value & cls.ADD:
            permissions.append(cls.ADD)
        if value & cls.DELETE:
            permissions.append(cls.DELETE)
        if value & cls.MODIFY:
            permissions.append(cls.MODIFY)
        if value & cls.SPECIAL:
            permissions.append(cls.SPECIAL)
        return permissions

    @classmethod
    def has_permission(cls, permission_value, category, permission):
        """判断用户是否具有某个分类的指定权限"""
        category_index = cls.CATEGORIES.index(category)
        category_value = (permission_value >> (category_index * 5)) & 0x1F  # 右移并取5位

        return category_value & permission > 0  # 使用位与运算判断权限是否存在
