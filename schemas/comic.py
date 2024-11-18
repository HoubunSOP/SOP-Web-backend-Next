from pydantic import BaseModel
from typing import List, Optional
from datetime import date


# 分类响应模型
class Category(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# 漫画作者响应模型
class ComicAuthor(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# 漫画详细信息响应模型
class ComicDetail(BaseModel):
    id: int
    name: str
    original_name: Optional[str]  # 漫画原名可以为空
    date: date
    intro: Optional[str]
    cover: str
    auto: bool
    author: ComicAuthor  # 包含作者信息
    categories: List[Category]  # 包含漫画的分类列表

    class Config:
        from_attributes = True


class ComicCreate(BaseModel):
    name: str
    original_name: Optional[str] = None
    author_name: str  # 作者名字
    date: date
    intro: Optional[str] = None
    cover: str
    auto: bool = False
    category_id: Optional[int] = None  # 分类 ID，可选字段
