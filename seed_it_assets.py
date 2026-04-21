from database import SessionLocal
from models import ITAsset, SoftwareAsset
from datetime import datetime

def seed_it():
    db = SessionLocal()
    
    # 1. Hardware Assets
    assets = [
        ITAsset(name="TheSharkEngine", type="Server", model="Dell Precision R7910", ip_address="192.168.1.245", status="Online", location="Server Rack"),
        ITAsset(name="Master Dev Machine", type="Laptop", model="Dell XPS", ip_address="192.168.1.18", status="Online", location="Office"),
        ITAsset(name="Field Unit", type="Mobile", model="iPhone 17 Pro Max", status="Online", notes="Primary Field Intake Device"),
        ITAsset(name="Automation Controller", type="PLC", model="Allen-Bradley L32E", ip_address="192.168.1.20", status="Online", location="Garden Control Box")
    ]
    
    try:
        db.add_all(assets)
        db.commit()
        
        # 2. Software (Link to Hardware)
        shark = db.query(ITAsset).filter(ITAsset.name == "TheSharkEngine").first()
        software = [
            SoftwareAsset(name="SQL Server Express", version="2022", vendor="Microsoft", installed_on=shark.asset_id),
            SoftwareAsset(name="PyCharm Professional", version="2024.1", vendor="JetBrains", installed_on=shark.asset_id),
            SoftwareAsset(name="Streamlit", version="1.32", vendor="Open Source", installed_on=shark.asset_id)
        ]
        db.add_all(software)
        db.commit()
        print("IT Infrastructure assets have been logged to the Nexus.")
    except Exception as e:
        print(f"Error seeding IT assets: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_it()
