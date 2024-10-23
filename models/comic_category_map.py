from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base

class ComicCategoryMap(Base):
    __tablename__ = 'comic_category_map'

    comic_id = Column(Integer, ForeignKey('comics.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)