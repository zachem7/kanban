from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/columns", tags=["Columns"])


@router.post("/", response_model=schemas.ColumnRead)
def create_column(payload: schemas.ColumnCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).get(payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    col = models.KanbanColumn(
        title=payload.title,
        position=payload.position,
        project=project
    )
    db.add(col)
    db.commit()
    db.refresh(col)
    return col


@router.get("/{column_id}", response_model=schemas.ColumnRead)
def get_column(column_id: int, db: Session = Depends(get_db)):
    col = db.query(models.KanbanColumn).get(column_id)
    if not col:
        raise HTTPException(status_code=404, detail="Column not found")
    return col


@router.get("/project/{project_id}", response_model=list[schemas.ColumnRead])
def get_columns_by_project(project_id: int, db: Session = Depends(get_db)):
    """Получить все колонки конкретного проекта"""
    return db.query(models.KanbanColumn).filter(models.KanbanColumn.project_id == project_id).all()