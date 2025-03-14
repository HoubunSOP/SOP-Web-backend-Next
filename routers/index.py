from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.article import Article
from models.category import Category
from models.comic import Comic, ComicAuthor
from models.magazine import Magazine
from schemas.calendar import ComicCalendarItem
from schemas.comic import NewComicsDetail
from tests.crawler.cherry_comic import to_mz
from utils.response import create_response

router = APIRouter()


@router.get("/calendar")
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
    ).order_by(Comic.date.desc()).all()

    # 返回漫画信息和是否已经发售（isComplete）
    comics_result = []
    for comic in comics_query:
        name = f"{comic.name} 第{comic.volume}卷"
        is_complete = comic.date <= today  # 如果发售日期小于等于今天，则已经发售
        comics_result.append(ComicCalendarItem(
            id=comic.id,
            name=name,
            original_name=comic.original_name,
            date=comic.date,
            cover=comic.cover,
            is_complete=is_complete
        ))

    return create_response(data=comics_result)


@router.get("/new_comics")
def get_new_comics(
        limit: int = Query(20, le=100, ge=1, description="输出数量(默认20)"),
        db: Session = Depends(get_db)
):
    # 查询正负90天内发售的漫画
    comics_query = db.query(Comic).order_by(Comic.date.desc()).limit(limit).all()

    # 返回漫画信息和是否已经发售（isComplete）
    comics_result = []
    for comic in comics_query:
        name = f"{comic.name} 第{comic.volume}卷"
        comics_result.append(NewComicsDetail(
            id=comic.id,
            name=name,
            original_name=comic.original_name,
            date=comic.date,
            cover=comic.cover,
        ))

    return create_response(data=comics_result)


@router.get("/recommended")
def get_recommended_articles(
        limit: int = Query(5, le=100, ge=1, description="推荐文章输出数量(默认5)"),
        db: Session = Depends(get_db)
):
    # 查询recommended为1的文章
    recommended_articles = db.query(Article).filter(Article.recommended == 1).limit(limit).all()

    if not recommended_articles:
        raise HTTPException(status_code=404, detail="没有推荐文章")

    return create_response(data=recommended_articles)


@router.get("/counts")
def get_counts(db: Session = Depends(get_db)):
    """
    获取杂志、文章、漫画、分类和漫画作者的总数量，以及 auto=1 的漫画数量
    """
    # 查询各个表的总数量
    article_count = db.query(Article).count()
    comic_count = db.query(Comic).count()
    category_count = db.query(Category).count()
    comic_author_count = db.query(ComicAuthor).count()
    magazine_count = db.query(Magazine).count()

    # 查询 auto=1 的漫画数量
    auto_comic_count = db.query(Comic).filter(Comic.auto == 1).count()

    # 返回结构化数据
    return create_response(data={
        "articles": article_count,
        "comics": comic_count,
        "categories": category_count,
        "comic_authors": comic_author_count,
        "magazines": magazine_count,
        "auto_comics": auto_comic_count
    })

# 爬虫触发路由
@router.get("/crawler")
def crawler(db: Session = Depends(get_db)):
   to_mz(db)
