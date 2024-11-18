# 获取漫画详情接口
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.category import Category
from models.comic import Comic, ComicAuthor
from schemas.comic import ComicDetail, ComicCreate
from utils.MarkdownRenderer import MarkdownRenderer

router = APIRouter()


@router.get("/comics/{comic_id}", response_model=ComicDetail)
def get_comic_detail(comic_id: int, edit: bool = False, db: Session = Depends(get_db)):
    """
    获取漫画详情接口，包括作者信息
    :param comic_id: 漫画ID
    :param edit: 是否为编辑模式，如果为 False，则渲染 intro 为 HTML
    """
    comic = db.query(Comic).join(ComicAuthor).filter(Comic.id == comic_id).first()
    if not comic:
        raise HTTPException(status_code=404, detail="漫画未找到")

    # 如果 edit 为 False，则将 intro 渲染为 HTML
    if not edit and comic.intro:
        renderer = MarkdownRenderer()
        comic.intro = renderer.render(comic.intro)

    return comic


@router.post("/comics")
def create_comic(comic: ComicCreate, db: Session = Depends(get_db)):
    # 如果未指定分类 ID，则使用默认分类 ID 为 5
    category_id = comic.category_id or 5

    # 检查分类是否存在
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # 查找或创建作者
    author = db.query(ComicAuthor).filter(ComicAuthor.name == comic.author_name).first()
    if not author:
        author = ComicAuthor(name=comic.author_name)
        db.add(author)
        db.commit()
        db.refresh(author)

    # 创建漫画实例
    new_comic = Comic(
        name=comic.name,
        original_name=comic.original_name,
        author_id=author.id,
        date=comic.date,
        intro=comic.intro,
        cover=comic.cover,
        auto=comic.auto,
    )

    # 关联分类
    new_comic.categories.append(category)

    # 保存到数据库
    db.add(new_comic)
    db.commit()
    db.refresh(new_comic)

    return new_comic


@router.put("/comics/{comic_id}")
def update_comic(comic_id: int, comic: ComicCreate, db: Session = Depends(get_db)):
    # 查找漫画
    db_comic = db.query(Comic).filter(Comic.id == comic_id).first()
    if not db_comic:
        raise HTTPException(status_code=404, detail="Comic not found")

    # 更新漫画字段
    db_comic.name = comic.name
    db_comic.original_name = comic.original_name
    db_comic.date = comic.date
    db_comic.intro = comic.intro
    db_comic.cover = comic.cover
    db_comic.auto = comic.auto

    # 查找或创建作者
    author = db.query(ComicAuthor).filter(ComicAuthor.name == comic.author_name).first()
    if not author:
        author = ComicAuthor(name=comic.author_name)
        db.add(author)
        db.commit()
        db.refresh(author)
    db_comic.author_id = author.id

    # 更新分类
    if comic.category_id:
        category = db.query(Category).filter(Category.id == comic.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        db_comic.categories = [category]
    elif not db_comic.categories:  # 如果漫画没有分类，设置默认分类为 5
        default_category = db.query(Category).filter(Category.id == 5).first()
        if not default_category:
            raise HTTPException(status_code=404, detail="Default category not found")
        db_comic.categories = [default_category]

    # 提交更新
    db.commit()
    db.refresh(db_comic)

    return db_comic


@router.delete("/comics/{comic_id}")
def delete_comic(comic_id: int, db: Session = Depends(get_db)):
    # 查找漫画
    db_comic = db.query(Comic).filter(Comic.id == comic_id).first()
    if not db_comic:
        raise HTTPException(status_code=404, detail="Comic not found")

    # 删除漫画
    db.delete(db_comic)
    db.commit()

    return {"detail": "Comic deleted successfully"}
