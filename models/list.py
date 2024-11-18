#models/list.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from models import Base

# 漫画模型
class Comics(Base):
    __tablename__ = "comics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    cover = Column(String(255), nullable=False)
    auto = Column(Integer, nullable=False)

# 文章模型
class Articles(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    cover = Column(String(255), nullable=True)

# 杂志模型
class Magazines(Base):
    __tablename__ = "magazines"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    publish_date = Column(Date, nullable=False)
    cover = Column(String(255), nullable=False)

# 分类表
class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

# 关联表
comic_category_map = Table(
    "comic_category_map",
    Base.metadata,
    Column("comic_id", Integer, ForeignKey("comics.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)
article_category_map = Table(
    "article_category_map",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)
magazine_category_map = Table(
    "magazine_category_map",
    Base.metadata,
    Column("magazine_id", Integer, ForeignKey("magazines.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)