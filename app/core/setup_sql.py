import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

user = os.getenv('AWS_RDS_MYSQL_DB_USERNAME')
password = os.getenv('AWS_RDS_MYSQL_DB_PASSWORD')
host = os.getenv('AWS_RDS_MYSQL_DB_HOST')
port = os.getenv('AWS_RDS_MYSQL_DB_PORT')
database = os.getenv('AWS_RDS_MYSQL_DB_DATABASE')
database_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

database_engine = create_engine(database_url)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)
Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
