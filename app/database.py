from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import config

POSTGRES_USERNAME = config.settings.POSTGRES_USERNAME
POSTGRES_PASSWORD = config.settings.POSTGRES_PASSWORD
POSTGRES_SERVER = config.settings.POSTGRES_SERVER
POSTGRES_DB = config.settings.POSTGRES_DB

# SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{postgresserver}/{db}"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
