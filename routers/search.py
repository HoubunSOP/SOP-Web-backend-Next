from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models.article import Article
from models.comic import Comic, ComicAuthor
from models.magazine import Magazine
from models.user import User
from models.category import Category, CategoryType

from schemas.search import ComicListItem, ArticleListItem, MagazineListItem, SearchResponse, CategoryListItem
from utils.response import create_response

router = APIRouter()


@router.get("/search")
def search_resources(
        query: str,
        resource_type: str = Query("all", description="搜索资源类型 ('comics', 'articles', 'magazines', 'all')"),
        page: int = Query(1, ge=1, description="当前页数，从 1 开始"),
        limit: int = Query(12, ge=1, le=100, description="每页显示的条目数"),
        db: Session = Depends(get_db),
):
    """
    通用搜索接口，可以在漫画、文章、杂志、分类等多个维度进行搜索，支持分页。
    :param query: 搜索关键字
    :param resource_type: 资源类型 ('comics', 'articles', 'magazines', 'all')
    :param page: 当前页数（默认为 1）
    :param limit: 每页条目数（默认为 12）
    """

    offset = (page - 1) * limit

    # 搜索漫画
    if resource_type == "comics" or resource_type == "all":
        comics_query = db.query(Comic).join(ComicAuthor).filter(
            or_(
                Comic.name.ilike(f"%{query}%"),
                Comic.original_name.ilike(f"%{query}%"),
                ComicAuthor.name.ilike(f"%{query}%"),
            )
        )
        total_comics = comics_query.count()  # 获取总条目数
        comics_query = comics_query.offset(offset).limit(limit).all()
        comics_result = [ComicListItem.model_validate(comic) for comic in comics_query]
    else:
        comics_result = []
        total_comics = 0

    # 搜索文章
    if resource_type == "articles" or resource_type == "all":
        articles_query = db.query(Article).join(User).filter(
            or_(
                Article.title.ilike(f"%{query}%"),
                User.username.ilike(f"%{query}%")
            )
        )
        total_articles = articles_query.count()  # 获取总条目数
        articles_query = articles_query.offset(offset).limit(limit).all()
        articles_result = [ArticleListItem.model_validate(article) for article in articles_query]
    else:
        articles_result = []
        total_articles = 0

    # 搜索杂志
    if resource_type == "magazines" or resource_type == "all":
        magazines_query = db.query(Magazine).filter(
            or_(
                Magazine.name.ilike(f"%{query}%")
            )
        )
        total_magazines = magazines_query.count()  # 获取总条目数
        magazines_query = magazines_query.offset(offset).limit(limit).all()
        magazines_result = [MagazineListItem.model_validate(magazine) for magazine in magazines_query]
    else:
        magazines_result = []
        total_magazines = 0

    # 同时搜索分类
    if resource_type == "all":
        # 通过 query 搜索分类名称
        categories_query = db.query(Category).join(CategoryType).filter(
            or_(
                Category.name.ilike(f"%{query}%"),
                CategoryType.name.ilike(f"%{query}%")
            )
        )
        total_categories = categories_query.count()  # 获取总条目数
        categories_query = categories_query.offset(offset).limit(limit).all()
        categories_result = [CategoryListItem.model_validate(category) for category in categories_query]
    else:
        categories_result = []
        total_categories = 0

    total_results = total_comics + total_articles + total_magazines + total_categories
    total_pages = (total_results + limit - 1) // limit  # 向上取整

    return create_response(data=SearchResponse(
        comics=comics_result,
        articles=articles_result,
        magazines=magazines_result,
        categories=categories_result,
        page=page,
        limit=limit,
        total_results=total_results,
        total_pages=total_pages,
    ))
