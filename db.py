from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

engine = create_engine("sqlite:///task_leave.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    tasks = relationship("Task", back_populates="user")
    leaves = relationship("Leave", back_populates="user")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String, default="Pending")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tasks")

class Leave(Base):
    __tablename__ = 'leaves'
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.date.today)
    reason = Column(String)
    approved = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="leaves")

def init_db():
    Base.metadata.create_all(bind=engine)
