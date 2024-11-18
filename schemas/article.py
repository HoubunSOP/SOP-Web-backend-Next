# schemas/article.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserDetail(BaseModel):
    id: int
    username: str
    user_avatar: Optional[str]
    user_bio: Optional[str]

    class Config:
        from_attributes = True

class Category(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ArticleDetail(BaseModel):
    id: int
    title: str
    date: date
    content: str
    cover: Optional[str]
    comic: Optional[str]
    recommended: bool
    author: UserDetail
    categories: List[Category]  # 添加分类字段

    class Config:
        from_attributes = True
