from datetime import datetime, timedelta
from typing import List

from models.comic import Comic
from schemas.calendar import ComicCalendarItem
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.article import Article
from schemas.article import ArticleRecommendationItem
from database import get_db

router = APIRouter()


@router.get("/calendar", response_model=List[ComicCalendarItem])
def get_comics_calendar(db: Session = Depends(get_db)):
    # 获取当前日期
    today = datetime.today().date()

    # 计算90天前和90天后的日期
    start_date = today - timedelta(days=90)
    end_date = today + timedelta(days=90)

    # 查询正负90天内发售的漫画
    comics_query = db.query(Comic).filter(
        Comic.date >= start_date,
        Comic.date <= end_date
    ).all()

    # 返回漫画信息和是否已经发售（isComplete）
    comics_result = []
    for comic in comics_query:
        is_complete = comic.date <= today  # 如果发售日期小于等于今天，则已经发售
        comics_result.append(ComicCalendarItem(
            id=comic.id,
            name=comic.name,
            original_name=comic.original_name,
            date=comic.date,
            cover=comic.cover,
            is_complete=is_complete
        ))

    return comics_result

@router.get("/recommended", response_model=List[ArticleRecommendationItem])
def get_recommended_articles(
        limit: int = Query(5, le=100, ge=1, description="推荐文章输出数量(默认5)"),
        db: Session = Depends(get_db)
):
    # 查询recommended为1的文章
    recommended_articles = db.query(Article).filter(Article.recommended == 1).limit(limit).all()

    if not recommended_articles:
        raise HTTPException(status_code=404, detail="没有推荐文章")

    return recommended_articles
