from pydantic import BaseModel
from datetime import date
from typing import List


# 漫画日历返回项
class ComicCalendarItem(BaseModel):
    id: int
    name: str
    original_name: str
    date: date
    cover: str
    is_complete: bool  # 是否已经发售

    class Config:
        from_attributes = True
