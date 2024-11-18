from pydantic import BaseModel
from typing import List, TypeVar, Generic
import datetime


# 漫画响应模型
class ComicListItem(BaseModel):
    id: int
    name: str
    date: datetime.date
    cover: str
    auto: int
    class Config:
        from_attributes = True


class ArticleListItem(BaseModel):
    id: int
    title: str
    date: datetime.date
    cover: str

    class Config:
        from_attributes = True


# 杂志响应模型
class MagazineListItem(BaseModel):
    id: int
    name: str
    publish_date: datetime.date
    cover: str

    class Config:
        from_attributes = True


# 创建一个类型变量，用于支持不同的资源类型
T = TypeVar('T', bound=BaseModel)

class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]  # 接受任何继承自 BaseModel 的类型
    total_pages: int
    current_page: int
