import datetime
from typing import List

from pydantic import BaseModel

from schemas.article import Category


# 漫画响应模型
class ComicListItem(BaseModel):
    id: int
    name: str
    date: datetime.date
    cover: str
    auto: int
    categories: List[Category]  # 添加分类字段

    class Config:
        from_attributes = True


class ArticleListItem(BaseModel):
    id: int
    title: str
    date: datetime.date
    cover: str
    recommended: bool
    categories: List[Category]  # 添加分类字段

    class Config:
        from_attributes = True


# 杂志响应模型
class MagazineListItem(BaseModel):
    id: int
    name: str
    publish_date: datetime.date
    cover: str
    categories: List[Category]  # 添加分类字段

    class Config:
        from_attributes = True
