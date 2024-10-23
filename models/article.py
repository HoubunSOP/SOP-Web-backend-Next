from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models.base import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    content = Column(String, nullable=True)
    cover = Column(String(255), nullable=True)
    comic = Column(String(255), nullable=True)
    recommended = Column(Boolean, nullable=False, default=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship("User", backref="articles")