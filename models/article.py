from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from models import Base

# 文章与分类的中间表
article_category_map = Table(
    "article_category_map",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

# 文章表
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="文章唯一标识")
    title = Column(String(255), nullable=False, comment="文章标题")
    date = Column(Date, nullable=False, comment="文章发布日期")
    content = Column(Text, nullable=True, comment="文章内容，支持Markdown语法")
    cover = Column(String(255), nullable=True, comment="文章封面")
    comic = Column(String(255), nullable=True, comment="关联漫画")
    recommended = Column(Boolean, default=False, comment="是否为推荐文章")
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="作者ID")

    author = relationship("User", back_populates="articles")
    categories = relationship("Category", secondary=article_category_map, back_populates="articles")
