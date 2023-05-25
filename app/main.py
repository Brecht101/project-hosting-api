import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="🔥Team CCS03🔥",description="Welcome to our API, all users and projects are stored in a database and passwords are hashed!!! Interactive with bash & ansible 🤯")

security = HTTPBasic()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/create")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/projects/create")
def create_project(project: schemas.ProjectCreate, username: str, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project, username=username)

@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/projects", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@app.get("/project", response_model=schemas.Project)
def read_project(id: int = Query(default=None,gt=0,
                             description="This parameter needs the private ID of a project."), db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Invalid ID")
    return db_project

@app.get("/user", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid username")
    return db_user

@app.delete("/projects/delete")
def delete_project(project_name: str, delete_volume: bool, db: Session = Depends(get_db)):
    return crud.delete_project(db=db, project_name=project_name, delete_volume=delete_volume)
