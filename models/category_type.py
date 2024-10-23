from sqlalchemy import Column, Integer, String
from models.base import Base

class CategoryType(Base):
    __tablename__ = 'category_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)