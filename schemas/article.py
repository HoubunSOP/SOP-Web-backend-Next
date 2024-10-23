from pydantic import BaseModel
from datetime import date

class ArticleCreate(BaseModel):
    title: str
    date: date
    content: str
    cover: str = None
    comic: str = None
    recommended: bool = False
    author_id: int

class Article(BaseModel):
    id: int
    title: str
    date: date
    content: str
    cover: str = None
    comic: str = None
    recommended: bool = False
    author_id: int

    class Config:
        orm_mode = True