from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.magazine import Magazine, magazine_category_map, magazine_comic_map
from models.category import Category
from utils.database import get_db
from schemas.magazine import MagazineDetail, MagazineCreate

from utils.MarkdownRenderer import MarkdownRenderer
from utils.response import create_response

router = APIRouter()


@router.get("/magazines/{magazine_id}")
def get_magazine_detail(magazine_id: int, edit: bool = False, db: Session = Depends(get_db)):
    """
    获取杂志详细信息接口，包括该杂志的漫画名称及分类。
    :param magazine_id: 杂志ID
    :param edit: 是否为编辑模式，如果为 False，则渲染 intro 为 HTML
    """
    # 查询杂志信息
    magazine = db.query(Magazine).filter(Magazine.id == magazine_id).first()
    if not magazine:
        raise HTTPException(status_code=404, detail="杂志未找到")
    # 如果 edit 为 False，则将 intro 渲染为 HTML
    if not edit and magazine.intro:
        renderer = MarkdownRenderer()
        magazine.intro = renderer.render(magazine.intro)

    # 获取与该杂志相关的漫画名称
    comic_names = db.query(magazine_comic_map.c.comic_name).filter(
        magazine_comic_map.c.magazine_id == magazine_id).all()
    comic_names = [comic_name[0] for comic_name in comic_names]  # 提取漫画名称列表

    # 获取与该杂志相关的分类
    category_ids = db.query(magazine_category_map.c.category_id).filter(
        magazine_category_map.c.magazine_id == magazine_id).all()
    category_ids = [category_id[0] for category_id in category_ids]  # 提取分类ID列表
    categories = db.query(Category).filter(Category.id.in_(category_ids)).all()  # 获取分类信息

    # 返回杂志详情、相关漫画名称和分类信息
    return create_response(data=MagazineDetail(
        magazine=magazine,
        comics=comic_names,
        categories=categories
    ))


@router.post("/magazines")
def create_magazine(magazine_data: MagazineCreate, db: Session = Depends(get_db)):
    """
    创建新的杂志，并关联漫画和分类。
    :param magazine_data: 包含杂志信息及漫画名称列表
    """
    # 检查是否已经存在该杂志名称
    existing_magazine = db.query(Magazine).filter(Magazine.name == magazine_data.name).first()
    if existing_magazine:
        raise HTTPException(status_code=400, detail="该杂志已存在")

    # 获取或创建默认分类（如果没有指定分类）
    category_id = magazine_data.category_id if magazine_data.category_id else 5
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类未找到")

    # 创建新杂志
    new_magazine = Magazine(
        name=magazine_data.name,
        cover=magazine_data.cover,
        publish_date=magazine_data.publish_date,
        intro=magazine_data.intro,
        link=magazine_data.link
    )
    db.add(new_magazine)
    db.commit()
    db.refresh(new_magazine)

    # 关联分类
    magazine_category = magazine_category_map.insert().values(
        magazine_id=new_magazine.id,
        category_id=category.id
    )
    db.execute(magazine_category)

    # 处理漫画名称列表
    for comic_name in magazine_data.comics:
        # 如果漫画名称不存在，新增
        existing_comic = db.query(magazine_comic_map).filter(
            magazine_comic_map.c.magazine_id == new_magazine.id,
            magazine_comic_map.c.comic_name == comic_name
        ).first()
        if not existing_comic:
            new_comic = magazine_comic_map.insert().values(
                magazine_id=new_magazine.id,
                comic_name=comic_name
            )
            db.execute(new_comic)

    db.commit()
    return create_response(message="杂志创建成功")


@router.put("/magazines/{magazine_id}")
def update_magazine(magazine_id: int, magazine_data: MagazineCreate, db: Session = Depends(get_db)):
    """
    更新杂志信息，并重新关联漫画和分类。
    :param magazine_id: 杂志ID
    :param magazine_data: 包含杂志信息及漫画名称列表
    """
    # 查询杂志
    magazine = db.query(Magazine).filter(Magazine.id == magazine_id).first()
    if not magazine:
        raise HTTPException(status_code=404, detail="杂志未找到")

    # 更新杂志信息
    magazine.name = magazine_data.name
    magazine.cover = magazine_data.cover
    magazine.publish_date = magazine_data.publish_date
    magazine.intro = magazine_data.intro
    magazine.link = magazine_data.link
    db.commit()

    # 更新分类
    category_id = magazine_data.category_id if magazine_data.category_id else 5
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类未找到")

    # 删除旧分类并插入新分类
    db.query(magazine_category_map).filter(magazine_category_map.c.magazine_id == magazine.id).delete()
    db.commit()
    magazine_category = magazine_category_map.insert().values(
        magazine_id=magazine.id,
        category_id=category.id
    )
    db.execute(magazine_category)

    # 删除原有漫画名称的关联
    db.query(magazine_comic_map).filter(magazine_comic_map.c.magazine_id == magazine.id).delete()

    # 重新插入漫画名称
    for comic_name in magazine_data.comics:
        new_comic = magazine_comic_map.insert().values(
            magazine_id=magazine.id,
            comic_name=comic_name
        )
        db.execute(new_comic)

    db.commit()
    return create_response(message="杂志更改成功")


@router.delete("/magazines/{magazine_id}")
def delete_magazine(magazine_id: int, db: Session = Depends(get_db)):
    """
    删除杂志信息，并删除与漫画的关联。
    :param magazine_id: 杂志ID
    """
    # 查询杂志
    magazine = db.query(Magazine).filter(Magazine.id == magazine_id).first()
    if not magazine:
        raise HTTPException(status_code=404, detail="杂志未找到")

    # 删除杂志与分类的关联
    db.query(magazine_category_map).filter(magazine_category_map.c.magazine_id == magazine_id).delete()

    # 删除杂志与漫画的关联
    db.query(magazine_comic_map).filter(magazine_comic_map.c.magazine_id == magazine_id).delete()

    # 删除杂志
    db.delete(magazine)
    db.commit()

    return create_response(message="杂志删除成功")
