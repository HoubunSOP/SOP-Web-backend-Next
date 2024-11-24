# 获取文章详情接口
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from models.article import Article, article_category_map
from models.category import Category
from models.user import User
from schemas.article import ArticleCreate
from utils.MarkdownRenderer import MarkdownRenderer
from utils.auth import ACCESS_SECURITY
from utils.response import create_response

router = APIRouter()


@router.get("/articles/{article_id}")
def get_article_detail(article_id: int, edit: bool = False, db: Session = Depends(get_db)):
    """
    获取文章详情接口
    :param article_id: 文章ID
    :param edit: 是否为编辑模式，如果为 False，则渲染 content 为 HTML
    """
    # 查询文章
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章未找到")

    # 渲染 content 为 HTML（如果需要）
    if not edit and article.content:
        renderer = MarkdownRenderer()
        article.content = renderer.render(article.content)

    # 获取分类信息
    category_ids = db.query(article_category_map.c.category_id).filter(
        article_category_map.c.article_id == article_id).all()
    category_ids = [category_id[0] for category_id in category_ids]  # 提取分类ID列表
    categories = db.query(Category).filter(Category.id.in_(category_ids)).all()

    # 获取作者信息
    user = db.query(User).filter(User.id == article.author_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="作者未找到")
    # 排除权限和权限组字段
    user_data = {
        "id": user.id,
        "username": user.username,
        "user_avatar": user.user_avatar,
        "user_bio": user.user_bio
    }

    # 构造返回数据
    article_data = {
        **article.__dict__,
        "categories": [{"id": category.id, "name": category.name} for category in categories],
        "author": user_data,
    }

    return create_response(data=article_data)


@router.post("/articles")
def create_article(article: ArticleCreate, db: Session = Depends(get_db),
                   credentials: JwtAuthorizationCredentials = Security(ACCESS_SECURITY)):
    # 如果未指定分类 ID，则使用默认分类 ID 为 6
    category_id = article.categories.id or 6

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
        author_id=credentials['id'],
    )

    # 关联分类
    new_article.categories.append(category)

    # 保存到数据库
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return create_response(message="文章创建成功")


@router.put("/articles/{article_id}")
def update_article(article_id: int, article: ArticleCreate, db: Session = Depends(get_db),
                   credentials: JwtAuthorizationCredentials = Security(ACCESS_SECURITY)):
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
    db_article.author_id = credentials['id']

    # 更新分类，如果提供了分类 ID
    if article.categories.id:
        category = db.query(Category).filter(Category.id == article.categories.id).first()
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

    return create_response(message="文章修改成功")


@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()

    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")

    # 删除文章
    db.delete(db_article)
    db.commit()

    return create_response(message="文章删除成功")
