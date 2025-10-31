from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=schemas.ProjectRead)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    project = models.Project(title=payload.title, description=payload.description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/", response_model=list[schemas.ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="project not found")
    return project

@router.post("/{project_id}/users/{user_id}", response_model=schemas.ProjectRead)
def add_user_to_project(project_id: int, user_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).get(project_id)
    user = db.query(models.User).get(user_id)
    if not project or not user:
        raise HTTPException(status_code=404, detail="project or user not found")
    if user in project.users:
        raise HTTPException(status_code=400, detail="user already in project")
    project.users.append(user)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}/users/{user_id}", response_model=schemas.ProjectRead)
def remove_user_from_project(project_id: int, user_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).get(project_id)
    user = db.query(models.User).get(user_id)
    if not project or not user:
        raise HTTPException(status_code=404, detail="project or user not found")
    if user not in project.users:
        raise HTTPException(status_code=400, detail="user not in project")
    project.users.remove(user)
    db.commit()
    db.refresh(project)
    return project
