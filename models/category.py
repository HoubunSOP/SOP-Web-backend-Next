from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

# 分类类型表
class CategoryType(Base):
    __tablename__ = "category_types"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="分类类型唯一标识")
    name = Column(String(255), nullable=False, comment="分类类型名称")

    categories = relationship("Category", back_populates="type")

# 分类表
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="分类唯一标识")
    name = Column(String(255), nullable=False, comment="分类名称")
    category_type = Column(Integer, ForeignKey("category_types.id", ondelete="CASCADE"), nullable=False, comment="分类类型ID")

    type = relationship("CategoryType", back_populates="categories")
    comics = relationship("Comic", secondary="comic_category_map", back_populates="categories")
    articles = relationship("Article", secondary="article_category_map", back_populates="categories")
    magazines = relationship("Magazine", secondary="magazine_category_map", back_populates="categories")
