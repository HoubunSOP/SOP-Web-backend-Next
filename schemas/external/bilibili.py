# bili专栏列表
from typing import List
from pydantic import BaseModel


class CVAuthor(BaseModel):
    mid: int
    name: str
    face: str


class CVArticle(BaseModel):
    id: int
    title: str
    banner_url: str
    author: CVAuthor
    image_urls: List[str]
    publish_time: int
    ctime: int
    mtime: int
    origin_image_urls: List[str]


class CVData(BaseModel):
    articles: List[CVArticle]
    pn: int
    ps: int
    count: int
