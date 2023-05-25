from datetime import datetime

from pydantic import BaseModel



class UserBase(BaseModel):
    first_name: str
    last_name: str
    user_id: int | None = None


class UserCreate(UserBase):
    password: str

class User(UserBase):

    class Config:
        orm_mode = True
        
class ProjectBase(BaseModel):
    project_name: str
    project_description: str
    project_id: int | None = None
    
class ProjectCreate(ProjectBase):
    database_root_password: str
    
class Project(ProjectBase):
    user_id: int
    class Config:
        orm_mode = True