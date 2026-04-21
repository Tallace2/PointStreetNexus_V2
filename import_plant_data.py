import pandas as pd
import numpy as np
from database import SessionLocal
from models import BotanicalRegistry, Planting, MediaAsset
import os

BACKUP_DIR = "backups"

def import_data():
    print("--- Importing Plant Data ---")
    db = SessionLocal()
    
    try:
        # 1. Import Botanical Registry
        reg_path = os.path.join(BACKUP_DIR, "botanical_registry_backup.csv")
        if os.path.exists(reg_path):
            df = pd.read_csv(reg_path)
            df = df.replace({np.nan: None})
            for _, row in df.iterrows():
                # We use db.merge() instead of db.add() so it safely overwrites or inserts
                # while preserving the exact original species_id.
                obj = BotanicalRegistry(**row.to_dict())
                db.merge(obj)
            db.commit()
            print(f"Imported Botanical Registry from {reg_path}")

        # 2. Import Plantings
        plant_path = os.path.join(BACKUP_DIR, "plantings_backup.csv")
        if os.path.exists(plant_path):
            df = pd.read_csv(plant_path)
            df = df.replace({np.nan: None})
            for _, row in df.iterrows():
                # Using db.merge() prevents Primary Key collisions if seed_data was already run
                obj = Planting(**row.to_dict())
                db.merge(obj)
            db.commit()
            print(f"Imported Plantings from {plant_path}")

        # 3. Import Media Assets
        media_path = os.path.join(BACKUP_DIR, "media_assets_backup.csv")
        if os.path.exists(media_path):
            df = pd.read_csv(media_path)
            df = df.replace({np.nan: None})
            for _, row in df.iterrows():
                obj = MediaAsset(**row.to_dict())
                db.merge(obj)
            db.commit()
            print(f"Imported Media Assets from {media_path}")

        print("--- Import Complete ---")

    except Exception as e:
        print(f"Error during import: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_data()
