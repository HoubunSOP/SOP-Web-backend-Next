# 获取文章详情接口
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.article import ArticleDetail
import models.user
import models.category
from models.article import Article
from database import get_db

router = APIRouter()

@router.get("/articles/{article_id}", response_model=ArticleDetail)
def get_article_detail(article_id: int, db: Session = Depends(get_db)):
    """
    获取文章详情接口
    :param article_id: 文章ID
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章未找到")
    return article