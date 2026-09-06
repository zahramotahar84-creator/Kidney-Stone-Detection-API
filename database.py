# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 09:07:39 2026

@author: user
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# آدرس دیتابیس (یک فایل به نام users.db در کنار پروژه ساخته می‌شود)
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# ساخت موتور دیتابیس
# connect_args={"check_same_thread": False} مخصوص دیتابیس SQLite است تا در FastAPI به مشکل نخوریم
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# ساخت Session برای ارتباط با دیتابیس
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# کلاس پایه برای تعریف مدل‌های دیتابیس
Base = declarative_base()

# مدل کاربر در دیتابیس (ساختار جدول کاربران)
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    image_path=Column(String,nullable=True)

# ساخت جداول در دیتابیس بر اساس مدل‌های تعریف شده
Base.metadata.create_all(bind=engine)

# --- Dependency یا وابستگی برای تزریق در توابع API ---
def get_db():
    db = SessionLocal()
    try:
        yield db # دیتابیس را تزریق می‌کند
    finally:
        db.close() # بعد از اتمام هر درخواست، اتصال را می‌بندد تا حافظه پر نشود