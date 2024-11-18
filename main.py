
from fastapi import FastAPI
from fastapi_login import LoginManager

from config import AUTH_SECRET
from routers import list, article, comic, magazine, category, search

app = FastAPI()
SECRET = AUTH_SECRET
manager = LoginManager(SECRET, "/login")

app.include_router(list.router, tags=["Search"])
app.include_router(search.router, tags=["Search"])
app.include_router(article.router, tags=["Article"])
app.include_router(comic.router, tags=["Comic"])
app.include_router(magazine.router, tags=["Magazine"])
app.include_router(category.router, tags=["Category"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
