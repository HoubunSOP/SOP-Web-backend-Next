from pydantic import BaseModel
from datetime import date

class ComicCreate(BaseModel):
    name: str
    author_id: int
    date: date
    intro: str = None
    cover: str
    auto: bool = False

class Comic(BaseModel):
    id: int
    name: str
    author_id: int
    date: date
    intro: str = None
    cover: str
    auto: bool = False

    class Config:
        orm_mode = True