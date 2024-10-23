from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base

class ArticleCategoryMap(Base):
    __tablename__ = 'article_category_map'

    article_id = Column(Integer, ForeignKey('articles.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)