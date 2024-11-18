from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


# 用户组表
class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户组唯一标识")
    group_name = Column(String(255), nullable=False, comment="用户组名称")
    permission_level = Column(Integer, nullable=False, comment="用户权限")

    users = relationship("User", back_populates="group")


# 用户表
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户唯一标识")
    username = Column(String(255), nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    user_avatar = Column(String(255), nullable=True, comment="用户头像")
    user_permission = Column(Integer, default=0, comment="用户权限")
    user_bio = Column(Text, nullable=True, comment="用户简介")
    user_position = Column(Integer, ForeignKey("user_groups.id", ondelete="SET NULL"), nullable=True,
                           comment="用户组ID")

    group = relationship("UserGroup", back_populates="users")
    articles = relationship("Article", back_populates="author")
