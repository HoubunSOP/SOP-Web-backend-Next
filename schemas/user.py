from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    user_avatar: Optional[str] = None
    user_bio: Optional[str] = None
    user_position: Optional[int] = None

    class Config:
        from_attributes = True


# 用户登录时的 Pydantic Schema
class UserLogin(BaseModel):
    username: str
    password: str
    aes: Optional[bool] = False
    iv: Optional[str] = None
