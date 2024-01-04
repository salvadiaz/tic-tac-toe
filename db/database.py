import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_DATABASE")
db_port = os.getenv("DB_PORT")
# URL_DATABASE = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
URL_DATABASE = f"mysql+pymysql://app_user:app_password@localhost:3306/app_db"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
