from database import SessionLocal
from models import Task
from datetime import datetime

def init_mission():
    db = SessionLocal()
    mission_tasks = [
        Task(name="Mission: Map Sunshine Garden (Inside/Outside)", task_type="Project", priority=1),
        Task(name="Sync Master Code to R7910 via Git", task_type="Infrastructure", priority=1),
        Task(name="Verify HEIC to JPG conversion on high-res iPhone photos", task_type="QA", priority=2),
        Task(name="Audit Plant.id data for 'Indoor/Outdoor' accuracy", task_type="Data", priority=2)
    ]
    try:
        db.add_all(mission_tasks)
        db.commit()
        print("Today's mission tasks have been logged to the SharkEngine database.")
    except Exception as e:
        print(f"Error logging tasks: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_mission()
