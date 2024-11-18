from pydantic import BaseModel
from typing import Optional


class CategoryTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryCountResponse(BaseModel):
    id: int
    name: str
    item_count: int  # 该分类下的项目数量
    category_type: CategoryTypeResponse  # 分类的类型（例如漫画、文章、杂志）

    class Config:
        from_attributes = True


# 创建分类时使用的模型
class CategoryCreate(BaseModel):
    name: str
    category_type: int

    class Config:
        from_attributes = True


# 更新分类时使用的模型
class CategoryUpdate(BaseModel):
    name: str
    category_type: int

    class Config:
        from_attributes = True