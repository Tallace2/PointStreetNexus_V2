from database import SessionLocal
from models import Task
from datetime import datetime

def add_grid_task():
    db = SessionLocal()
    try:
        new_task = Task(
            name="10x20 Grid Mapping (Nano 300 / iPhone 17)",
            task_type="To-Do",
            priority=2,
            is_completed=False,
            due_date=datetime(2024, 5, 1)
        )
        db.add(new_task)
        db.commit()
        print("Added '10x20 Grid Mapping' to your SQL Todo list.")
    finally:
        db.close()

if __name__ == "__main__":
    add_grid_task()
