from typing import Optional

from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.category import Category, CategoryType
from models.comic import comic_category_map
from models.magazine import magazine_category_map
from models.article import article_category_map
from schemas.category import CategoryCountResponse, CategoryTypeResponse

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
            item_count = db.query(article_category_map).filter(article_category_map.c.category_id == category.id).count()
        elif category.type.name == "杂志":
            # 查询该分类下的杂志数量
            item_count = db.query(magazine_category_map).filter(magazine_category_map.c.category_id == category.id).count()

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
