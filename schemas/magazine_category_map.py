from pydantic import BaseModel

class MagazineCategoryMap(BaseModel):
    magazine_id: int
    category_id: int

    class Config:
        orm_mode = True