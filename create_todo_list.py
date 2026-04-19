from database import SessionLocal
from models import Task, Project
from datetime import datetime, timedelta

def create_suggestions_todo():
    db = SessionLocal()
    try:
        # Get the current project
        proj = db.query(Project).filter(Project.name == "Spring 2024 Garden Expansion").first()
        proj_id = proj.project_id if proj else None

        suggestions = [
            {"name": "Implement PLC Logic (EtherNet/IP Valve Control)", "priority": 1, "type": "Automation"},
            {"name": "Setup Hubitat Maker API Integration (Live Moisture)", "priority": 1, "type": "IoT"},
            {"name": "Process 10x20 LiDAR Grid Scans (Nano 300 / IP17)", "priority": 2, "type": "Mapping"},
            {"name": "Weekly Plant Refresh Script (Health & Status Tracking)", "priority": 2, "type": "Maintenance"},
            {"name": "Build Media Ingestion Tool (IP17 Photo -> SQL)", "priority": 1, "type": "Media"},
            {"name": "Link 3D Models (GLB/USDZ) to Property Grid", "priority": 3, "type": "Modeling"},
            {"name": "BOM & Cost Tracking Dashboard", "priority": 2, "type": "Finance"}
        ]

        for s in suggestions:
            new_task = Task(
                project_id=proj_id,
                name=s["name"],
                priority=s["priority"],
                task_type=s["type"],
                due_date=datetime.now() + timedelta(days=7)
            )
            db.add(new_task)
        
        db.commit()
        print("Successfully created the suggestions TODO list in the database!")
        
    except Exception as e:
        print(f"Error creating tasks: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_suggestions_todo()
