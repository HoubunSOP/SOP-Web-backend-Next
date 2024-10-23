from pydantic import BaseModel

class MagazineComicMap(BaseModel):
    magazine_id: int
    comic_id: int

    class Config:
        orm_mode = True