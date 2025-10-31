from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1)

class UserRead(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class ProjectRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    users: List[UserRead] = []
    class Config:
        orm_mode = True

class ColumnCreate(BaseModel):
    title: str
    position: Optional[int] = 0
    project_id: int

class ColumnRead(BaseModel):
    id: int
    title: str
    position: int
    project_id: int
    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[int] = 0
    assignee_id: Optional[int] = None
    column_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    assignee_id: Optional[int] = None
    column_id: Optional[int] = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    assignee: Optional[UserRead] = None
    column_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class TaskLogRead(BaseModel):
    id: int
    task_id: int
    message: str
    created_at: datetime
    class Config:
        orm_mode = True
