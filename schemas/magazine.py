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
    comics: Optional[List[str]]  # 漫画名称列表
    categories: Optional[List[CategorySchema]]  # 分类名称列表

    class Config:
        from_attributes = True
