from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Comic(Base):
    __tablename__ = 'comics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('comic_authors.id'), nullable=False)
    date = Column(Date, nullable=False)
    intro = Column(String, nullable=True)
    cover = Column(String(255), nullable=False)
    auto = Column(Boolean, nullable=False, default=False)

    author = relationship("ComicAuthor", backref="comics")