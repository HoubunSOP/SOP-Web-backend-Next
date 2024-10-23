from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    category_type_id: int

class Category(BaseModel):
    id: int
    name: str
    category_type_id: int

    class Config:
        orm_mode = True