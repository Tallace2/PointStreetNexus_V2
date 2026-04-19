from database import SessionLocal
from models import IoTHub, PLCNode

def update_infrastructure():
    db = SessionLocal()
    try:
        # 1. Update Home Hub (C-8 Pro)
        home_hub = db.query(IoTHub).filter(IoTHub.name.like("%Home%")).first()
        if home_hub:
            home_hub.ip_address = "192.168.1.78"
            home_hub.api_key = "4c6c4a40-7115-45e7-88b2-7e1ac4312609"
            home_hub.model = "171" 
            print(f"Updated Hub: {home_hub.name}")
        
        # 2. Update Marina Hub (C-8)
        marina_hub = db.query(IoTHub).filter(IoTHub.name.like("%Marina%")).first()
        if marina_hub:
            marina_hub.ip_address = "192.168.1.62"
            marina_hub.api_key = "501bf0a4-01e0-4e8f-8e71-c9dcadea858d"
            marina_hub.model = "100"
            print(f"Updated Hub: {marina_hub.name}")
            
        # 3. Update PLC Node IP (New Static IP)
        plc = db.query(PLCNode).filter(PLCNode.name.like("%Irrigation%")).first()
        if plc:
            plc.ip_address = "192.168.1.201"
            print(f"Updated PLC: {plc.name} to new static IP {plc.ip_address}")
            
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_infrastructure()
