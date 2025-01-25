from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_ADDRESS, DATABASE_BASENAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PROT

DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_ADDRESS}:{DATABASE_PROT}/{DATABASE_BASENAME}"

# 配置引擎
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 检查连接是否有效
    pool_recycle=3600,   # 连接回收时间
    pool_size=10,        # 连接池大小
    max_overflow=20      # 最大溢出连接
)

# 配置会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    每次请求都会创建和释放数据库连接
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
