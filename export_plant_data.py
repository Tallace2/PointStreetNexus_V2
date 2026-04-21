import pandas as pd
from database import engine
from models import BotanicalRegistry, Planting, MediaAsset
import os

BACKUP_DIR = "backups"
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def export_data():
    print("--- Exporting Plant Data ---")
    
    try:
        # Export BotanicalRegistry
        df_registry = pd.read_sql("SELECT * FROM Botanical_Registry", engine)
        if not df_registry.empty:
            registry_path = os.path.join(BACKUP_DIR, "botanical_registry_backup.csv")
            df_registry.to_csv(registry_path, index=False)
            print(f"Exported {len(df_registry)} Botanical Registry entries to {registry_path}")
        else:
            print("No Botanical Registry data to export.")

        # Export Plantings
        df_plantings = pd.read_sql("SELECT * FROM Plantings", engine)
        if not df_plantings.empty:
            plantings_path = os.path.join(BACKUP_DIR, "plantings_backup.csv")
            df_plantings.to_csv(plantings_path, index=False)
            print(f"Exported {len(df_plantings)} Planting entries to {plantings_path}")
        else:
            print("No Planting data to export.")

        # Export Media Assets (only metadata, not the actual image files)
        df_media = pd.read_sql("SELECT * FROM Media_Assets", engine)
        if not df_media.empty:
            media_path = os.path.join(BACKUP_DIR, "media_assets_backup.csv")
            df_media.to_csv(media_path, index=False)
            print(f"Exported {len(df_media)} Media Asset entries to {media_path}")
        else:
            print("No Media Asset data to export.")
            
        print("--- Export Complete ---")

    except Exception as e:
        print(f"Error during export: {e}")

if __name__ == "__main__":
    export_data()
