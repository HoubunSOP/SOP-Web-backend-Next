from pydantic import BaseModel

class ComicCategoryMap(BaseModel):
    comic_id: int
    category_id: int

    class Config:
        orm_mode = True