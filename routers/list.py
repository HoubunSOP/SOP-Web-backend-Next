from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.list import Comics, Articles, Magazines, comic_category_map, article_category_map, magazine_category_map
from schemas.list import (
    PaginationResponse,
    ComicListItem,
    ArticleListItem,
    MagazineListItem,
)

router = APIRouter()

@router.get("/list/{resource_type}", response_model=PaginationResponse)
def list_resources(
    resource_type: str,
    limit: int = Query(12, ge=1, le=100, description="每页条数"),
    page: int = Query(1, ge=1, description="页码"),
    category_id: int = Query(None, description="分类ID（可选）"),
    db: Session = Depends(get_db),
):
    """
    通用列表接口，支持分页和分类筛选。
    :param db:
    :param resource_type: 资源类型 (comic, articles, magazines)
    :param limit: 每页条数
    :param page: 当前页码
    :param category_id: 分类ID
    """
    # 资源类型与模型、Schema、关联表的映射
    model_map = {
        "comics": (Comics, ComicListItem, comic_category_map),
        "articles": (Articles, ArticleListItem, article_category_map),
        "magazines": (Magazines, MagazineListItem, magazine_category_map),
    }

    if resource_type not in model_map:
        raise HTTPException(status_code=400, detail="无效的资源类型")

    model, schema, category_map = model_map[resource_type]

    # 构建查询
    query = db.query(model)

    if category_id is not None:
        # 按分类ID过滤
        query = query.join(category_map, model.id == category_map.c[resource_type + "_id"]) \
                     .filter(category_map.c.category_id == category_id)

    # 分页逻辑
    total_count = query.count()
    total_pages = (total_count + limit - 1) // limit
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    # 数据格式化
    result = []
    for item in items:
        try:
            print(schema.from_orm(item))
            result.append(schema.from_orm(item))
        except Exception as e:
            print(f"from_orm 失败：{item}, 错误：{e}")
    print(result)
    return {
        "items": result,
        "total_pages": total_pages,
        "current_page": page,
    }
