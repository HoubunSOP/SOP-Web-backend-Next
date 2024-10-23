from pydantic import BaseModel

class ComicAuthorCreate(BaseModel):
    name: str

class ComicAuthor(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True