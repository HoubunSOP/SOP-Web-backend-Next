from sqlalchemy import Column, Integer, String
from models.base import Base

class ComicAuthor(Base):
    __tablename__ = 'comic_authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)