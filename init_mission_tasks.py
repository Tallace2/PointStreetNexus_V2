from database import SessionLocal
from models import Task
from datetime import datetime, UTC

def init_mission():
    db = SessionLocal()
    
    mission_tasks = [
        Task(name="Mission: Map Sunshine Garden (Inside/Outside)", task_type="Project", priority=1, created_at=datetime.now(UTC)),
        Task(name="Sync Master Code to R7910 via Git", task_type="Infrastructure", priority=1, created_at=datetime.now(UTC)),
        Task(name="Verify HEIC to JPG conversion on high-res iPhone photos", task_type="QA", priority=2, created_at=datetime.now(UTC)),
        Task(name="Audit Plant.id data for 'Indoor/Outdoor' accuracy", task_type="Data", priority=2, created_at=datetime.now(UTC)),
        Task(name="DEV_Task: Establish Git Push/Pull pipeline between XPS and R7910", task_type="Development", priority=1, created_at=datetime.now(UTC)),
        Task(name="DEV_Task: Implement robust 'Architect's Sweep' for USGS API", task_type="Development", priority=2, created_at=datetime.now(UTC)),
        Task(name="DEV_Task: Fix OperationalError by confirming R7910 SQL Services", task_type="Development", priority=1, created_at=datetime.now(UTC)),
        Task(name="DEV_Task: Build V3 Enterprise UI with Categorized Navigation", task_type="Development", priority=1, created_at=datetime.now(UTC)),
        Task(name="DEV_Task: Implement Property Zones and System Glossary Tables", task_type="Development", priority=1, created_at=datetime.now(UTC)),
        Task(name="DEV_Task: Build Infrastructure Management System (IMS) for IT Assets", task_type="Development", priority=2, created_at=datetime.now(UTC)),
        Task(name="DEV_Task: Integrate 3D Property Grid with Plotly Graph Objects", task_type="Development", priority=1, created_at=datetime.now(UTC)),
        Task(name="DEV_Task: Create Supply & Product Inventory Table (CRUD)", task_type="Development", priority=2, created_at=datetime.now(UTC)),
        Task(name="DEV_Task: Fix Intake Queue Pathing for S-Drive vs C-Drive Failover", task_type="Development", priority=1, created_at=datetime.now(UTC))
    ]
    
    try:
        # Avoid duplicate tasks for the mission
        existing_task_names = [t.name for t in db.query(Task).all()]
        tasks_to_add = [t for t in mission_tasks if t.name not in existing_task_names]
        
        if tasks_to_add:
            db.add_all(tasks_to_add)
            db.commit()
            print(f"Added {len(tasks_to_add)} new mission/dev tasks to the SharkEngine database.")
        else:
            print("All mission tasks are already present in the database.")
            
    except Exception as e:
        print(f"Error logging tasks: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_mission()
