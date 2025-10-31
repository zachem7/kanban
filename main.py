from fastapi import FastAPI
from .database import Base, engine
from .routers import users, projects, columns, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kanban Backend (modular)")

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(columns.router)
app.include_router(tasks.router)
