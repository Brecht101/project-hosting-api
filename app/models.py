from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    first_name = Column(String(50))
    last_name = Column(String(50))
    password = Column(String(150))
    username = Column(String(100), unique=True)
    user_id = Column(Integer, primary_key=True, index=True)
    project=relationship("Project", back_populates="user")
    
class Project(Base):
    __tablename__ = "project"
    project_name = Column(String(100), unique=True)
    project_description = Column(String(100))
    database_root_password = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    project_id = Column(Integer, primary_key=True, index=True)
    user = relationship("User", back_populates="project")