from sqlalchemy import Column, Integer, String, Date
from models.base import Base

class Magazine(Base):
    __tablename__ = 'magazines'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    cover = Column(String(255), nullable=False)
    publish_date = Column(Date, nullable=False)
    intro = Column(String, nullable=True)
    link = Column(String(255), nullable=True)