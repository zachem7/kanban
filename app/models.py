from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import relationship
from .database import Base

# Ассоциативная таблица "многие ко многим" между пользователями и проектами
user_project_table = Table(
    "user_project",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

    projects = relationship("Project", secondary=user_project_table, back_populates="users")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")

    columns = relationship("KanbanColumn", back_populates="project", cascade="all, delete-orphan")
    users = relationship("User", secondary=user_project_table, back_populates="projects")


class KanbanColumn(Base):
    __tablename__ = "columns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    position = Column(Integer, default=0)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    project = relationship("Project", back_populates="columns")
    tasks = relationship("Task", back_populates="column", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    priority = Column(Integer, default=0)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    column_id = Column(Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)

    column = relationship("KanbanColumn", back_populates="tasks")
    assignee = relationship("User")
    logs = relationship("TaskLog", back_populates="task", cascade="all, delete-orphan")


class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="logs")