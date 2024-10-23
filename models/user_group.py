from sqlalchemy import Column, Integer, String, Integer
from models.base import Base

class UserGroup(Base):
    __tablename__ = 'user_groups'

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(100), nullable=False)
    permissions = Column(Integer, nullable=False)