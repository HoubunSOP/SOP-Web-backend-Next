from pydantic import BaseModel

class UserGroupCreate(BaseModel):
    group_name: str
    permissions: int

class UserGroup(BaseModel):
    id: int
    group_name: str
    permissions: int

    class Config:
        orm_mode = True