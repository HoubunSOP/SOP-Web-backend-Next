from pydantic import BaseModel
from typing import List, Optional

from schemas.comic import ComicAuthor


class ComicListItem(BaseModel):
    id: int
    name: str
    original_name: Optional[str] = None
    cover: str
    author: ComicAuthor  # 漫画作者

    class Config:
        from_attributes = True


class ArticleListItem(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    user: str  # 文章的用户

    class Config:
        from_attributes = True


class MagazineListItem(BaseModel):
    id: int
    name: str
    cover: str

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    comics: List[ComicListItem]
    articles: List[ArticleListItem]
    magazines: List[MagazineListItem]
    categories: List[str]  # 分类名称列表
    page: int
    limit: int
    total_results: int
    total_pages: int

    class Config:
        from_attributes = True
