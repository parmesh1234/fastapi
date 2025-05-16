from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///../todossapp.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:test1234@localhost/TodoApplicatonDatabase"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This correct_args is only for SQLite only

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()