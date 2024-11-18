from typing import Optional

from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.category import Category, CategoryType
from models.comic import comic_category_map, Comic
from models.magazine import magazine_category_map, Magazine
from models.article import article_category_map, Article
from schemas.category import CategoryCountResponse, CategoryTypeResponse, CategoryCreate, CategoryUpdate

router = APIRouter()


@router.get("/categories", response_model=list[CategoryCountResponse])
def get_categories(
        category_type_id: Optional[int] = Query(None, description="分类类型 ID（可选）"),
        db: Session = Depends(get_db),
):
    """
    获取所有分类信息，包括分类ID、名称和该分类下的项目数量。
    :param category_type_id: 分类类型 ID（例如：1 为漫画，2 为文章，3 为杂志）
    """
    # 查询所有分类并连接到 CategoryType 表
    query = db.query(Category).join(CategoryType).all()

    # 如果传入了 category_type_id，则根据 category_type_id 进行筛选
    if category_type_id:
        query = [category for category in query if category.type.id == category_type_id]

    if not query:
        raise HTTPException(status_code=404, detail="未找到匹配的分类")

    # 获取每个分类下的项目数量
    category_counts = []
    for category in query:
        item_count = 0
        if category.type.name == "漫画":
            # 查询该分类下的漫画数量
            item_count = db.query(comic_category_map).filter(comic_category_map.c.category_id == category.id).count()
        elif category.type.name == "文章":
            # 查询该分类下的文章数量
            item_count = db.query(article_category_map).filter(
                article_category_map.c.category_id == category.id).count()
        elif category.type.name == "杂志":
            # 查询该分类下的杂志数量
            item_count = db.query(magazine_category_map).filter(
                magazine_category_map.c.category_id == category.id).count()

        # 将 CategoryType 信息传递给 CategoryCountResponse
        category_counts.append(
            CategoryCountResponse(
                id=category.id,
                name=category.name,
                item_count=item_count,
                category_type=CategoryTypeResponse(id=category.type.id, name=category.type.name)
            )
        )

    return category_counts


@router.post("/categories")
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    """
    创建分类，确保没有重复的分类名称。
    :param category_data: 分类名称和分类类别
    """
    # 检查分类类型是否存在
    category_type = db.query(CategoryType).filter(CategoryType.id == category_data.category_type).first()
    if not category_type:
        raise HTTPException(status_code=400, detail="分类类型不存在")

    # 检查分类是否已存在
    existing_category = db.query(Category).filter(
        Category.name == category_data.name,
        Category.category_type == category_data.category_type
    ).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="该分类已存在")

    # 创建新的分类
    new_category = Category(
        name=category_data.name,
        category_type=category_data.category_type
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category  # 返回的是SQLAlchemy对象，FastAPI会自动转换为Pydantic模型


@router.put("/categories/{category_id}")
def update_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    """
    更新分类的名称和类别。
    :param category_id: 分类ID
    :param category_data: 分类名称和类别
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类未找到")

    # 检查分类类型是否存在
    category_type = db.query(CategoryType).filter(CategoryType.id == category_data.category_type).first()
    if not category_type:
        raise HTTPException(status_code=400, detail="分类类型不存在")

    # 更新分类信息
    category.name = category_data.name
    category.category_type = category_data.category_type
    db.commit()
    db.refresh(category)
    return category  # 返回的是SQLAlchemy对象，FastAPI会自动转换为Pydantic模型


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    删除分类。如果该分类下还有文章、漫画、杂志等关联内容，禁止删除。
    :param category_id: 分类ID
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类未找到")

    # 检查该分类是否有关联的文章、漫画、杂志
    related_articles = db.query(Article).filter(Article.categories.any(id=category_id)).all()
    related_comics = db.query(Comic).filter(Comic.categories.any(id=category_id)).all()
    related_magazines = db.query(Magazine).filter(Magazine.categories.any(id=category_id)).all()

    if related_articles or related_comics or related_magazines:
        raise HTTPException(
            status_code=400,
            detail="该分类下有关联的文章、漫画或杂志，无法删除。请先将其转移到其他分类。"
        )

    # 删除分类
    db.delete(category)
    db.commit()
    return {"detail": "分类已删除"}
