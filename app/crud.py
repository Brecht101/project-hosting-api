from sqlalchemy.orm import Session

import models
import schemas
import auth
import os
import subprocess


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.project_id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password,
        user_id=user.user_id,
        username=user.first_name + user.last_name
    )
    subprocess.run(["/ansible/create_users.sh", "-u", user.first_name + user.last_name, "-p", user.password])
    db.add(db_user)
    db.commit()
    return "User created your username is: " + user.first_name + user.last_name

def create_project(db: Session, username: str, project: schemas.ProjectCreate):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
       user_id = user.user_id
    db_project = models.Project(
        project_name=project.project_name,
        project_description=project.project_description,
        database_root_password=project.database_root_password,
        user_id=user_id,
        project_id=project.project_id
    )
    check_project = db.query(models.Project).filter(models.Project.project_name == project.project_name).first()
    if check_project:
       return "Project already exists!"
    subprocess.run(["/ansible/create_project.sh", project.project_name, project.database_root_password, "phpmyadmin-" + project.project_name + ".com", project.project_name + ".com", user.username]) 
    db.add(db_project)
    db.commit()
    return "Project created domain: " + project.project_name + ".com and phpmyadmin portal: phpmyadmin-" + project.project_name + ".com"

def delete_project(db: Session, project_name: str, delete_volume: bool):
    db_project = db.query(models.Project).filter(models.Project.project_name == project_name).first()
    user = db.query(models.User).filter(models.User.user_id == db_project.user_id).first()
    if db_project is None:
        return "Invalid project"
    if delete_volume is False:
       subprocess.run(["/ansible/delete_project.sh", db_project.project_name, db_project.database_root_password, "phpmyadmin-" + db_project.project_name + ".com", db_project.project_name + ".com", user.username, "nee"])
    if delete_volume is True:
       subprocess.run(["/ansible/delete_project.sh", db_project.project_name, db_project.database_root_password, "phpmyadmin-" + db_project.project_name + ".com", db_project.project_name + ".com", user.username, "ja"])
    db.delete(db_project)
    db.commit()
    return "Project deleted"
