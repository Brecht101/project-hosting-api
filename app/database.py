from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlitedb/sqlitedata.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://brecht:ccs03!@localhost:3306/users"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()