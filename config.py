import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()
# 尝试从环境变量中获取配置值
DATABASE_BASENAME = os.getenv("DATABASE_BASENAME")
DATABASE_ADDRESS = os.getenv("DATABASE_ADDRESS")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PROT = os.getenv("DATABASE_PROT")
AUTH_SECRET = os.getenv("AUTH_SECRET")