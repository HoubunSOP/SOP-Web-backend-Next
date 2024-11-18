from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.magazine import Magazine, magazine_category_map, magazine_comic_map
from models.category import Category
from database import get_db
from schemas.magazine import MagazineDetail

router = APIRouter()


@router.get("/magazines/{magazine_id}", response_model=MagazineDetail)
def get_magazine_detail(magazine_id: int, db: Session = Depends(get_db)):
    """
    获取杂志详细信息接口，包括该杂志的漫画名称及分类。
    :param magazine_id: 杂志ID
    """
    # 查询杂志信息
    magazine = db.query(Magazine).filter(Magazine.id == magazine_id).first()
    if not magazine:
        raise HTTPException(status_code=404, detail="杂志未找到")

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
    return MagazineDetail(
        magazine=magazine,
        comics=comic_names,
        categories=categories
    )
