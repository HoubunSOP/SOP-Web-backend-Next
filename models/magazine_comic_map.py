from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base


class MagazineComicMap(Base):
    __tablename__ = 'magazine_comic_map'

    magazine_id = Column(Integer, ForeignKey('magazines.id'), primary_key=True)
    comic_id = Column(Integer, ForeignKey('comics.id'), primary_key=True)