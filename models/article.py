#models/article.py
from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True, comment="分类唯一标识")
    name = Column(String(255), nullable=False, comment="分类名称")

    # 反向引用文章
    articles = relationship("models.article.Article", secondary="article_category_map", back_populates="categories")

class Article(Base):
    __tablename__ = "articles"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True, comment="文章唯一标识")
    title = Column(String(255), nullable=False, comment="文章标题")
    date = Column(Date, nullable=False, comment="文章发布日期")
    content = Column(Text, comment="文章内容，支持Markdown语法")
    cover = Column(String(255), nullable=True, comment="文章封面")
    comic = Column(String(255), nullable=True, comment="关联漫画")
    recommended = Column(Boolean, default=False, comment="是否为推荐文章")
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="作者ID")

    author = relationship("User", back_populates="articles")
    # 文章和分类的多对多关系
    categories = relationship("models.article.Category", secondary="article_category_map", back_populates="articles")


class ArticleCategoryMap(Base):
    __tablename__ = "article_category_map"
    __table_args__ = {"extend_existing": True}
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True, comment="用户唯一标识")
    username = Column(String(255), nullable=False, comment="用户名")
    user_avatar = Column(String(255), nullable=True, comment="用户头像")
    user_bio = Column(Text, nullable=True, comment="用户简介")

    articles = relationship("Article", back_populates="author")
