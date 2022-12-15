import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.getenv('POSTGRES_USERNAME')
password = os.getenv('POSTGRES_PASSWORD')
postgresserver = os.getenv('POSTGRES_SERVER')
db = os.getenv('POSTGRES_DB')

# SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{postgresserver}/{db}"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{postgresserver}/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
