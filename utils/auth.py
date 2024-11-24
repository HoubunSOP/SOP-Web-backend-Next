import base64
from datetime import timedelta

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from fastapi_jwt import JwtAccessBearerCookie
from passlib.context import CryptContext

from config import AUTH_SECRET

SECRET = AUTH_SECRET
ACCESS_TOKEN_EXPIRE_days = 30
ACCESS_SECURITY = JwtAccessBearerCookie(
    secret_key=AUTH_SECRET,
    auto_error=True,
    access_expires_delta=timedelta(days=ACCESS_TOKEN_EXPIRE_days)
)
AES_KEY = "?D}mznE=g^MW-i45"

# 创建一个密码上下文对象，用来加密和验证密码
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 加密密码
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def decrypt(enc: str, iv: str, key: str = AES_KEY) -> str:
    iv = base64.b64decode(iv)  # 解码IV
    enc = enc.encode("utf-8")
    enc = base64.b64decode(enc)  # 解码加密文本
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

    return unpad(cipher.decrypt(enc), AES.block_size).decode()


if __name__ == "__main__":
    encrypted_text = 'IEKVTVJv/MtBOPdxT5TMBA=='
    iv = 'vPJfRbuz/QLLMnxehitQew=='
    print(decrypt(encrypted_text, iv))
