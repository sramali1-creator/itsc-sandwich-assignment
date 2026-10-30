import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import conf

# DATABASE_URL can be set (e.g. to a SQLite URL) to override the MySQL connection, which the tests use.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") or (
    f"mysql+pymysql://{conf.db_user}:{quote_plus(conf.db_password)}"
    f"@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4"
)

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def _enable_sqlite_fks(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
