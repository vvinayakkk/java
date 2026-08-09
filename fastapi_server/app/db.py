import logging
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

def ensure_mysql_database():
    try:
        conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            connect_timeout=3
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{settings.MYSQL_DATABASE}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
        logger.info(f"Database '{settings.MYSQL_DATABASE}' ensured in MySQL.")
        return True
    except Exception as e:
        logger.warning(f"Could not connect to MySQL server: {e}")
        return False

use_mysql = ensure_mysql_database()
if use_mysql:
    db_url = settings.DATABASE_URL
    engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=3600)
else:
    db_url = "sqlite:///./adtech_crawler.db"
    logger.warning("Falling back to local SQLite database adtech_crawler.db")
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    if not SessionLocal:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    if engine:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info(f"Database tables initialized successfully on: {db_url}")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
