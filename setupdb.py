# setup_db.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL
DATABASE_URL = "sqlite:///./test.db"

# Create an engine and a base class
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)
