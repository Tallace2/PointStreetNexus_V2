from database import SessionLocal, engine
from models import (Base, MediaAsset, SensorReading, Planting, BotanicalRegistry, 
                   Task, GardenBed, PLCNode, PLCTag, IoTHub, IoTDevice, 
                   Project, ProjectBOM, OrderDetail, Order, Quote, Supplier, Manufacturer, Contact, PropertyGridNode)
import os
import shutil

MEDIA_DIR = "media"

def cleanup_data():
    print("--- 🧹 Commencing Database Cleanup ---")
    
    # 1. Clear Photos
    if os.path.exists(MEDIA_DIR):
        print(f"Clearing files in {MEDIA_DIR}...")
        for filename in os.listdir(MEDIA_DIR):
            file_path = os.path.join(MEDIA_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    
    # 2. Clear Database Tables (Order matters for Foreign Keys)
    db = SessionLocal()
    try:
        print("Deleting transactional records...")
        
        # Delete in order to avoid FK violations
        db.query(MediaAsset).delete()
        db.query(SensorReading).delete()
        db.query(Task).delete()
        db.query(ProjectBOM).delete()
        db.query(OrderDetail).delete()
        db.query(Order).delete()
        db.query(Quote).delete()
        
        # Delete Plantings before Species
        db.query(Planting).delete()
        db.query(BotanicalRegistry).delete()
        
        # Infrastructure and Projects (Soft delete these if you want to keep setup)
        # Uncomment these if you want to wipe EVERYTHING but keep tables
        # db.query(PLCTag).delete()
        # db.query(PLCNode).delete()
        # db.query(IoTDevice).delete()
        # db.query(IoTHub).delete()
        # db.query(GardenBed).delete()
        # db.query(PropertyGridNode).delete()
        # db.query(Project).delete()
        
        db.commit()
        print("SUCCESS: Transactional data and media cleared. Infrastructure setup preserved.")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_data()
