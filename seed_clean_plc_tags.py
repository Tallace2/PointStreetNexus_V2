from database import SessionLocal
from models import PLCNode, PLCTag

def seed_clean_tags():
    db = SessionLocal()
    try:
        # 1. Get the PLC
        plc = db.query(PLCNode).filter(PLCNode.name.like("%Irrigation%")).first()
        if not plc:
            print("PLC not found. Please run seed_data.py first.")
            return

        # 2. Delete old tags to start fresh
        db.query(PLCTag).filter(PLCTag.plc_id == plc.plc_id).delete()
        print("Cleaned old PLC tags.")

        # 3. Define the New Clean Interface
        new_tags = [
            PLCTag(plc_id=plc.plc_id, tag_name="PSN_Heartbeat", data_type="INT", description="Watchdog from Python"),
            PLCTag(plc_id=plc.plc_id, tag_name="PSN_Auto_Mode", data_type="BOOL", description="Master Remote/Auto switch"),
            PLCTag(plc_id=plc.plc_id, tag_name="PSN_System_Status", data_type="INT", description="0=Idle, 1=Watering, 2=Fault"),
        ]

        # Add RB Solenoids
        for i in range(1, 7):
            new_tags.append(PLCTag(plc_id=plc.plc_id, tag_name=f"PSN_RB{i}_Water_Cmd", data_type="BOOL", description=f"Solenoid for RB-{i}"))

        # Add Tote Solenoids
        for i in range(1, 4):
            new_tags.append(PLCTag(plc_id=plc.plc_id, tag_name=f"PSN_Tote{i}_Water_Cmd", data_type="BOOL", description=f"Solenoid for Tote-{i}"))

        db.add_all(new_tags)
        db.commit()
        print("Successfully seeded New Clean PLC Interface tags!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_clean_tags()
