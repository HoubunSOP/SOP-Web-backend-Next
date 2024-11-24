from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class Magazine(BaseModel):
    id: int
    name: str
    cover: str
    publish_date: date
    intro: Optional[str] = None
    link: Optional[str] = None

    class Config:
        from_attributes = True


class MagazineDetail(BaseModel):
    magazine: Magazine
    comics: Optional[List[str]]
    categories: Optional[List[CategorySchema]]

    class Config:
        from_attributes = True

class MagazineCreate(BaseModel):
    name: str
    publish_date: date
    cover: Optional[str] = None
    intro: Optional[str] = None
    link: Optional[str] = None
    comics: Optional[List[str]]
    category_id: Optional[int] = None