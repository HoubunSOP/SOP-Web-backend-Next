from fastapi_jwt import JwtAccessBearerCookie, JwtAuthorizationCredentials
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.user import UserLogin, UserCreate
from utils.Permission import Permission
from utils.auth import verify_password, hash_password
from datetime import timedelta
from config import AUTH_SECRET

SECRET = AUTH_SECRET
ACCESS_TOKEN_EXPIRE_days = 30

access_security = JwtAccessBearerCookie(
    secret_key=AUTH_SECRET,
    auto_error=True,
    access_expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_days)
)
router = APIRouter()


# 用户登录
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    # 获取用户信息
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise InvalidCredentialsException

    # 验证密码
    if not verify_password(data.password, user.password):
        raise InvalidCredentialsException

    # 创建 Token
    access_token = access_security.create_access_token(
        subject={"id": user.id, "name": user.username, "permissions": user.user_permission,
                 "user_group": user.user_position})
    return {"access_token": access_token}


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")

    # 默认设置权限为0，用户组为4，头像为空，简介为空
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        password=hashed_password,
        user_avatar=user.user_avatar or None,
        user_bio=user.user_bio or None,
        user_position=4  # 默认用户组为4
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"detail": "用户创建完成"}


from fastapi import Depends, HTTPException, status, Request


@router.put("/users/me")
def update_user(user: UserCreate, db: Session = Depends(get_db),
                credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = credentials['id']
    # 获取当前用户
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 只允许修改头像和简介，不允许修改权限
    db_user.username = user.username
    db_user.password = hash_password(user.password)  # 密码可以修改
    db_user.user_avatar = user.user_avatar or db_user.user_avatar  # 如果为空保持原样
    db_user.user_bio = user.user_bio or db_user.user_bio  # 如果为空保持原样

    db.commit()
    db.refresh(db_user)

    return {"detail": "资料更新成功"}


@router.get("/users")
def get_users(skip: int = Query(0, ge=0), limit: int = Query(15, le=100), db: Session = Depends(get_db),
              credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials or not Permission.has_permission(credentials['permissions'], 'user', Permission.READ):
        print(credentials['permissions'])
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 获取总数
    total_users = db.query(User).count()

    # 获取分页数据
    users = db.query(User).offset(skip).limit(limit).all()

    # 计算总页数
    total_pages = (total_users + limit - 1) // limit

    return {
        "total_users": total_users,
        "total_pages": total_pages,
        "users": users
    }


@router.put("/users/{user_id}")
def update_user_by_admin(user_id: int, user: UserCreate, db: Session = Depends(get_db),
                         credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials or not Permission.has_permission(credentials['permissions'], 'user', Permission.MODIFY):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 修改用户资料，包括权限
    db_user.username = user.username
    db_user.password = hash_password(user.password)  # 密码可以修改
    db_user.user_avatar = user.user_avatar or db_user.user_avatar  # 如果为空保持原样
    db_user.user_bio = user.user_bio or db_user.user_bio  # 如果为空保持原样
    db_user.user_position = user.user_position  # 管理员可以修改权限

    db.commit()
    db.refresh(db_user)

    return {"message": "User updated successfully"}
