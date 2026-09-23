from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal, Task


# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI()

# Location of our HTML files
templates = Jinja2Templates(directory="backend/templates")


# Show all tasks
@app.get("/")
def home(request: Request):
    db: Session = SessionLocal()

    tasks = db.query(Task).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tasks": tasks
        }
    )


# Add a new task
@app.post("/add")
def add_task(title: str = Form(...)):
    db: Session = SessionLocal()

    new_task = Task(title=title)

    db.add(new_task)
    db.commit()

    db.close()

    return RedirectResponse(url="/", status_code=303)


# Delete a task
@app.post("/delete/{task_id}")
def delete_task(task_id: int):
    db: Session = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if task:
        db.delete(task)
        db.commit()

    db.close()

    return RedirectResponse(url="/", status_code=303)


# Complete a task
@app.post("/complete/{task_id}")
def complete_task(task_id: int):
    db: Session = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if task:
        task.completed = True
        db.commit()

    db.close()

    return RedirectResponse(url="/", status_code=303)


# Toggle task completion using the checkbox
@app.post("/toggle/{task_id}")
def toggle_task(task_id: int):
    db: Session = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if task:
        task.completed = not task.completed
        db.commit()

    db.close()

    return RedirectResponse(url="/", status_code=303)