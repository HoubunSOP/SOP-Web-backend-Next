from fastapi_jwt import JwtAccessBearerCookie
from passlib.context import CryptContext

from datetime import timedelta
from config import AUTH_SECRET

SECRET = AUTH_SECRET
ACCESS_TOKEN_EXPIRE_days = 30
ACCESS_SECURITY = JwtAccessBearerCookie(
    secret_key=AUTH_SECRET,
    auto_error=True,
    access_expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_days)
)

# 创建一个密码上下文对象，用来加密和验证密码
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 加密密码
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
