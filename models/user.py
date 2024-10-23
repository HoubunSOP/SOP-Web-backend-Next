from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    user_avatar = Column(String(255), nullable=True)
    user_bio = Column(String, nullable=True)
    group_id = Column(Integer, ForeignKey('user_groups.id'), nullable=False)

    group = relationship("UserGroup", backref="users")