from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category_type_id = Column(Integer, ForeignKey('category_types.id'), nullable=False)

    category_type = relationship("CategoryType", backref="categories")