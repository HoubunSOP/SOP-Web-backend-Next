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
    name: Optional[str] = None

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


class ArticleRecommendationItem(BaseModel):
    id: int
    title: str
    content: str
    cover: str
    date: date
    recommended: bool

    class Config:
        from_attributes = True


class ArticleCreate(BaseModel):
    title: str
    date: date
    content: Optional[str] = None
    cover: Optional[str] = None
    comic: Optional[str] = None
    recommended: bool = False
    categories: Optional[Category] = None  # 分类 ID，可选字段


class ArticleResponse(ArticleCreate):
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
