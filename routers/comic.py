from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.comic import Comics, ComicAuthors
from schemas.comic import ComicDetail

router = APIRouter()

# 获取漫画详细信息及作者
@router.get("/comics/{comic_id}", response_model=ComicDetail)
def get_comic_detail(comic_id: int, db: Session = Depends(get_db)):
    comic = db.query(Comics).join(ComicAuthors).filter(Comics.id == comic_id).first()
    if comic is None:
        raise HTTPException(status_code=404, detail="Comic not found")
    return comic
