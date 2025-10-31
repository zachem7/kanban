from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..utils import create_task_log

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskRead)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    col = db.query(models.KanbanColumn).get(payload.column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")

    assignee = None
    if payload.assignee_id:
        assignee = db.query(models.User).get(payload.assignee_id)
        if not assignee:
            raise HTTPException(status_code=404, detail="Assignee not found")

    task = models.Task(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        assignee=assignee,
        column=col,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    create_task_log(db, task, f"Task created: '{task.title}'")
    return task


@router.get("/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/{task_id}/logs", response_model=List[schemas.TaskLogRead])
def get_task_logs(task_id: int, db: Session = Depends(get_db)):
    return db.query(models.TaskLog).filter(models.TaskLog.task_id == task_id).all()