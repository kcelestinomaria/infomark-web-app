import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db, username: str, email: str, password: str):
    hashed_password = hash_password(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

def get_user(db, username: str):
    return db.query(User).filter(User.username == username).first()

def update_user_details(db, username: str, new_name: str, new_email: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.username = new_name
        user.email = new_email
        db.commit()
        db.refresh(user)
        return True
    return False

def reset_password(db, username: str, new_password: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.hashed_password = hash_password(new_password)
        db.commit()
        db.refresh(user)
        return True
    return False

def login(username: str, password: str):
    db = next(get_db())
    user = get_user(db, username)
    if user and verify_password(password, user.hashed_password):
        st.session_state['user'] = user.username
        return True
    return False

def logout():
    st.session_state.pop('user', None)
    st.experimental_rerun()
