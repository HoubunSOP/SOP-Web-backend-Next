# 获取文章详情接口
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.article import ArticleDetail, ArticleCreate, ArticleResponse
import models.user
from models.category import Category
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

@router.post("/articles")
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    # 如果未指定分类 ID，则使用默认分类 ID 为 5
    category_id = article.category_id or 5

    # 检查分类是否存在
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # 创建文章实例
    new_article = Article(
        title=article.title,
        date=article.date,
        content=article.content,
        cover=article.cover,
        comic=article.comic,
        recommended=article.recommended,
        author_id=article.author_id,
    )

    # 关联分类
    new_article.categories.append(category)

    # 保存到数据库
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article

@router.put("/articles/{article_id}")
def update_article(article_id: int, article: ArticleCreate, db: Session = Depends(get_db)):
    # 获取文章
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")

    # 更新文章字段
    db_article.title = article.title
    db_article.date = article.date
    db_article.content = article.content
    db_article.cover = article.cover
    db_article.comic = article.comic
    db_article.recommended = article.recommended
    db_article.author_id = article.author_id

    # 更新分类，如果提供了分类 ID
    if article.category_id:
        category = db.query(Category).filter(Category.id == article.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        db_article.categories = [category]
    elif not db_article.categories:  # 如果文章没有分类，设置默认分类为 5
        default_category = db.query(Category).filter(Category.id == 5).first()
        if not default_category:
            raise HTTPException(status_code=404, detail="Default category not found")
        db_article.categories = [default_category]

    # 提交更新
    db.commit()
    db.refresh(db_article)

    return db_article


@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()

    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")

    # 删除文章
    db.delete(db_article)
    db.commit()

    return db_article
