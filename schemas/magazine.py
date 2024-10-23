from pydantic import BaseModel
from datetime import date

class MagazineCreate(BaseModel):
    name: str
    cover: str
    publish_date: date
    intro: str = None
    link: str = None

class Magazine(BaseModel):
    id: int
    name: str
    cover: str
    publish_date: date
    intro: str = None
    link: str = None

    class Config:
        orm_mode = True