from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base

class MagazineCategoryMap(Base):
    __tablename__ = 'magazine_category_map'

    magazine_id = Column(Integer, ForeignKey('magazines.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)