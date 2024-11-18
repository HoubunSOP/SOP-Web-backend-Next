from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from models import Base

# 杂志与分类的中间表
magazine_category_map = Table(
    "magazine_category_map",
    Base.metadata,
    Column("magazine_id", Integer, ForeignKey("magazines.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

# 杂志与漫画的中间表
magazine_comic_map = Table(
    "magazine_comic_map",
    Base.metadata,
    Column("magazine_id", Integer, ForeignKey("magazines.id", ondelete="CASCADE"), primary_key=True),
    Column("comic_name", String(255), nullable=False, primary_key=True, comment="漫画名称"),
)


class Magazine(Base):
    __tablename__ = "magazines"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="杂志唯一标识")
    name = Column(String(255), nullable=False, comment="杂志名称")
    cover = Column(String(255), nullable=False, comment="杂志封面")
    publish_date = Column(Date, nullable=False, comment="杂志发布时间")
    intro = Column(Text, nullable=True, comment="杂志简介")
    link = Column(String(255), nullable=True, comment="杂志链接")

    categories = relationship("Category", secondary=magazine_category_map, back_populates="magazines")
