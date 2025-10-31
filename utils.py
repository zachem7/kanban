from sqlalchemy.orm import Session
from .models import Task, TaskLog

def create_task_log(db: Session, task: Task, message: str):
    log = TaskLog(task_id=task.id, message=message)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
