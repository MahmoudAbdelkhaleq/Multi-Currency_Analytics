import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from fastapi import FastAPI
# Dependency

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()