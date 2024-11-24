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
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    user: Optional[str] = None  # 文章的用户

    class Config:
        from_attributes = True


class MagazineListItem(BaseModel):
    id: int
    name: str
    cover: str

    class Config:
        from_attributes = True

class CategoryTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryListItem(BaseModel):
    id: int
    name: str
    type: CategoryTypeResponse

    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    comics: List[ComicListItem]
    articles: List[ArticleListItem]
    magazines: List[MagazineListItem]
    categories: List[CategoryListItem]
    page: int
    limit: int
    total_results: int
    total_pages: int

    class Config:
        from_attributes = True
