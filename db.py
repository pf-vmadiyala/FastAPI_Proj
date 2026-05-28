
"""
db.py — HOW WE TALK TO MYSQL (connection layer)

Mental model:
  This file does NOT know about "products" or routes.
  It only: read secrets → build URL → open pool → hand out sessions.

  app.py asks for a session → SessionLocal() → you run queries → close session.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Base = registry for all SQLAlchemy table classes (see app/models.py).
# Every ORM model inherits from this ONE Base so SQLAlchemy knows they exist.
Base = declarative_base()

# Load DB_USER, DB_PASSWORD, etc. from .env into os.environ
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

DB_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# engine = long-lived connection pool to MySQL (created once at import time)
# echo=True prints SQL in terminal — great for learning, turn off in production
engine = create_engine(DB_URL, echo=True)

# SessionLocal = factory: each call SessionLocal() gives you ONE workspace (session)
# autocommit=False → changes are not saved until you db.commit()
# autoflush=False → SQL is not sent early unless you flush/commit
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
