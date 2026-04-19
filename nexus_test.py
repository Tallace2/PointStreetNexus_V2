from database import engine, SessionLocal
from models import Base, Task
from datetime import datetime

def run_test():
    print("--- Starting Nexus Connection Test ---")
    
    try:
        # 1. Ensure tables exist
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] Connected to PointStreetNexusDB")

        # 2. Test a simple write to Tasks
        db = SessionLocal()
        new_test_task = Task(
            name=f"Connection Test {datetime.now().strftime('%H:%M:%S')}",
            task_type="System Test",
            is_completed=True
        )
        db.add(new_test_task)
        db.commit()
        print(f"[SUCCESS] Wrote test task to SQL Server.")
        db.close()

    except Exception as e:
        print(f"[FAILED] Connection error: {e}")

if __name__ == "__main__":
    run_test()
