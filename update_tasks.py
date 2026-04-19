from database import SessionLocal
from models import Task
from datetime import datetime

def seed_future_tasks():
    db = SessionLocal()
    tasks = [
        Task(name="Advanced 3D Visualizer for 10x20 Nano 300 Grid", task_type="To-Do", priority=2),
        Task(name="PLC Automation: Sync Hubitat moisture to Solenoid control", task_type="To-Do", priority=1),
        Task(name="Media Enhancement: Thermal image overlay support", task_type="To-Do", priority=3),
        Task(name="Implement AI 'Simulation Mode' to save API credits during UI testing", task_type="To-Do", priority=1)
    ]
    try:
        db.add_all(tasks)
        db.commit()
        print("Future tasks added to SQL table.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_future_tasks()
