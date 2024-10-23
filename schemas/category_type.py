from pydantic import BaseModel

class CategoryTypeCreate(BaseModel):
    name: str

class CategoryType(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True