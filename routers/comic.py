# 获取漫画详情接口
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.comic import Comic, ComicAuthor
from schemas.comic import ComicDetail

router = APIRouter()

@router.get("/comics/{comic_id}", response_model=ComicDetail)
def get_comic_detail(comic_id: int, db: Session = Depends(get_db)):
    """
    获取漫画详情接口，包括作者信息
    :param comic_id: 漫画ID
    """
    comic = db.query(Comic).join(ComicAuthor).filter(Comic.id == comic_id).first()
    if not comic:
        raise HTTPException(status_code=404, detail="漫画未找到")
    return comic