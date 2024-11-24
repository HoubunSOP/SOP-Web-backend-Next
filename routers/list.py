from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.article import Article, article_category_map
from models.category import Category
from models.comic import Comic, comic_category_map
from models.magazine import Magazine, magazine_category_map
from schemas.list import (
    ComicListItem,
    ArticleListItem,
    MagazineListItem,
)
from utils.response import create_response

router = APIRouter()

@router.get("/list/{resource_type}")
def list_resources(
        resource_type: str,
        limit: int = Query(12, ge=1, le=100, description="每页条数"),
        page: int = Query(1, ge=1, description="页码"),
        category_id: int = Query(None, description="分类ID（可选）"),
        db: Session = Depends(get_db),
):
    """
    通用资源列表接口，支持分页与分类筛选。
    :param resource_type: 资源类型 ('comics', 'articles', 'magazines')
    """
    # 模型与Schema映射
    model_map = {
        "comics": (Comic, ComicListItem, comic_category_map),
        "articles": (Article, ArticleListItem, article_category_map),
        "magazines": (Magazine, MagazineListItem, magazine_category_map),
    }

    if resource_type not in model_map:
        raise HTTPException(status_code=400, detail="无效的资源类型")

    model, schema, category_map = model_map[resource_type]

    # 构建查询
    query = db.query(model).join(category_map, model.id == category_map.c[resource_type[:-1] + "_id"]) \
        .join(Category, Category.id == category_map.c.category_id)

    if category_id is not None:
        # 分类筛选
        query = query.filter(category_map.c.category_id == category_id)
    query = query.order_by(model.date.desc())
    # 分页逻辑
    total_count = query.count()
    total_pages = (total_count + limit - 1) // limit
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    # 数据格式化：将分类信息加入到每个资源项中
    result = []
    for item in items:
        item_schema = schema.from_orm(item)
        categories = item.categories # 获取分类名称
        item_schema.categories = categories  # 将分类信息添加到响应中
        result.append(item_schema)

    return create_response(data={
        "items": result,
        "total_pages": total_pages,
        "current_page": page,
    })
