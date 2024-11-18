# models/comic.py

from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

# 漫画作者模型
class ComicAuthors(Base):
    __tablename__ = 'comic_authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    # 在作者模型中反向引用漫画模型
    comics = relationship('models.comic.Comics', back_populates='author')


# 漫画模型
class Comics(Base):
    __tablename__ = 'comics'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    original_name = Column(String, nullable=True)  # 新增漫画原名字段
    date = Column(Date, nullable=False)
    intro = Column(Text, nullable=True)
    cover = Column(String, nullable=False)
    auto = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey('comic_authors.id'), nullable=False)  # 外键关联漫画作者

    # 在漫画模型中引用漫画作者
    author = relationship('ComicAuthors', back_populates='comics')

    # 与分类表的多对多关系
    categories = relationship('models.comic.Categories', secondary='comic_category_map', back_populates='comics')

# 分类模型
class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # 反向引用漫画模型
    comics = relationship('models.comic.Comics', secondary='comic_category_map', back_populates='categories')

# 中间表：漫画分类关联表
class ComicCategoryMap(Base):
    __tablename__ = 'comic_category_map'
    __table_args__ = {"extend_existing": True}
    comic_id = Column(Integer, ForeignKey('comics.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
