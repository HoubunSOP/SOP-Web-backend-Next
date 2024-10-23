from pydantic import BaseModel

class ArticleCategoryMap(BaseModel):
    article_id: int
    category_id: int

    class Config:
        orm_mode = True