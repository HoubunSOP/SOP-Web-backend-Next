from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    user_avatar: str = None
    user_bio: str = None
    group_id: int

class User(BaseModel):
    id: int
    username: str
    user_avatar: str = None
    user_bio: str = None
    group_id: int

    class Config:
        orm_mode = True