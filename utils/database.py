import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import DATABASE_ADDRESS, DATABASE_BASENAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PROT, DATABASE_TYPE

if DATABASE_TYPE == "sqlite":
    DATABASE_URL = f"sqlite:///{os.path.dirname(os.path.abspath(__file__))}/database/{DATABASE_BASENAME}.db"
elif DATABASE_TYPE == "mysql":
    DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_ADDRESS}:{DATABASE_PROT}/{DATABASE_BASENAME}"
else:
    print("数据库配置出现问题，请检查配置文件")
    exit(1)

# 配置引擎
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 检查连接是否有效
    pool_recycle=3600,  # 连接回收时间
    pool_size=10,  # 连接池大小
    max_overflow=20  # 最大溢出连接
)

# 配置会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_and_initialize_db(db):
    """
    检查数据库是否初始化，如果没有，执行安装 SQL 脚本
    """
    try:
        # 尝试查询表
        result = db.execute("SELECT 1 FROM comics LIMIT 1;")  # 你可以替换为你想查询的表或者条件
        # 如果表存在，表示数据库已经初始化
        return True
    except Exception:  # 如果数据库不存在该表或其他查询错误，说明未初始化
        return False


def initialize_db(db):
    """
    从 install.sql 文件导入 SQL 语句并执行
    """
    if DATABASE_TYPE == "sqlite":
        install_sql_path = '../database/install_sqlite.sql'
    else:
        install_sql_path = '../database/install.sql'

    if os.path.exists(install_sql_path):
        with open(install_sql_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # 执行 SQL 脚本
        db.execute(text(sql_script))
        db.commit()
        print("数据库已初始化")
    else:
        print("安装 SQL 脚本未找到，无法初始化数据库。")


def get_db():
    """
    每次请求都会创建和释放数据库连接
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
