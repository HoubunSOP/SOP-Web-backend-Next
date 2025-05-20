from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from routers import list, article, comic, magazine, category, search, index, user
from utils.meiliclient import init_indices
from utils.response import http_exception_handler, generic_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    try:
        await init_indices()
    except Exception as e:
        print(f'初始化失败：{e}')
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)
# 注册异常处理器
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.include_router(list.router, tags=["Search"])
app.include_router(search.router, tags=["Search"])
app.include_router(article.router, tags=["Article"])
app.include_router(comic.router, tags=["Comic"])
app.include_router(magazine.router, tags=["Magazine"])
app.include_router(category.router, tags=["Category"])
app.include_router(user.router, tags=["User"])
app.include_router(index.router)

origins = [
    "http://sop.sakurakoi.top",
    "https://sop.sakurakoi.top",
    "https://www.fwgxt.top",
    "https://fwgxt.top",
    "http://www.fwgxt.top",
    "http://fwgxt.top",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:3001",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
