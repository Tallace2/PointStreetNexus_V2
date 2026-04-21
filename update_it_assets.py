from database import SessionLocal
from models import ITAsset, SoftwareAsset
import json

def update_assets():
    db = SessionLocal()
    
    try:
        # Add a test asset to ensure the table works
        new_asset = ITAsset(
            name="Network Switch - Point Street",
            type="Network",
            model="Cisco SG350",
            ip_address="192.168.1.5",
            status="Online",
            location="Basement Rack"
        )
        db.add(new_asset)
        db.commit()
        print("Successfully added new IT Asset to SQL Server.")
        
    except Exception as e:
        print(f"Error updating assets: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_assets()
