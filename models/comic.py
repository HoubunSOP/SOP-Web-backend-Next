from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from models import Base

# 漫画与分类的中间表
comic_category_map = Table(
    "comic_category_map",
    Base.metadata,
    Column("comic_id", Integer, ForeignKey("comics.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

# 漫画表
class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="漫画唯一标识")
    name = Column(String(255), nullable=False, comment="漫画名称")
    original_name = Column(String(255), nullable=True, comment="漫画原名")
    author_id = Column(Integer, ForeignKey("comic_authors.id", ondelete="CASCADE"), nullable=False, comment="漫画作者ID")
    date = Column(Date, nullable=False, comment="漫画发布日期")
    intro = Column(Text, comment="漫画简介，支持Markdown语法")
    cover = Column(String(255), nullable=False, comment="封面图片文件名")
    auto = Column(Boolean, default=False, nullable=False, comment="是否为自动生成")

    author = relationship("ComicAuthor", back_populates="comics")
    categories = relationship("Category", secondary=comic_category_map, back_populates="comics")

# 漫画作者表
class ComicAuthor(Base):
    __tablename__ = "comic_authors"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="漫画作者唯一标识")
    name = Column(String(255), nullable=False, comment="漫画作者名称")

    comics = relationship("Comic", back_populates="author")
