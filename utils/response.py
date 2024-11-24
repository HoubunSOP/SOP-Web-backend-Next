from typing import Union

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Query, DeclarativeMeta


# 统一成功响应
def create_response(data: Union[BaseModel, dict, list, Query, None] = None, message: str = "Success"):
    """
    统一响应体格式：
    - data 支持 Pydantic 模型、dict、list 或 SQLAlchemy 查询结果。
    """
    # 如果是 SQLAlchemy Base 模型或查询结果，将其转为字典
    if isinstance(data, DeclarativeMeta):  # 检查是否是 SQLAlchemy 模型
        data = {column.name: getattr(data, column.name) for column in data.__table__.columns}
    elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], DeclarativeMeta):
        data = [{column.name: getattr(item, column.name) for column in item.__table__.columns} for item in data]
    elif isinstance(data, BaseModel):  # 如果是 Pydantic 模型，转换为字典
        data = data.model_dump()

    return {
        "status": status.HTTP_200_OK,
        "message": message,
        "detail": data or {}
    }


# HTTP异常处理器
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content={
            "status": exc.status_code,
            "message": exc.detail if isinstance(exc.detail, str) else "Error",
            "detail": {}
        },
        status_code=exc.status_code
    )


# 通用异常处理器
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content={
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Server Error",
            "detail": {"error": str(exc)}
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
