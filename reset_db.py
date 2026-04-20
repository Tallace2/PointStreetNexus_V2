import pyodbc
import os
import shutil
from database import init_db

# SQL Server Configuration - POINTING TO R7910
SERVER = '192.168.1.245,55658'
DATABASE = 'PointStreetNexusDB'
USERNAME = 'sa'
PASSWORD = 'Bailey9751'
MEDIA_DIR = "media"

def force_reset_database():
    print(f"--- Force Resetting Database on {SERVER} ---")
    
    # 1. Clear the local Media Folder
    if os.path.exists(MEDIA_DIR):
        print(f"Cleaning media folder: {MEDIA_DIR}")
        for filename in os.listdir(MEDIA_DIR):
            file_path = os.path.join(MEDIA_DIR, filename)
            try:
                if os.path.isfile(file_path): os.unlink(file_path)
            except Exception as e: print(f"Error: {e}")
    
    # 2. Connect to MASTER on R7910 to drop the DB
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE=master;"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    
    try:
        conn = pyodbc.connect(connection_string, autocommit=True)
        cursor = conn.cursor()
        
        print("Closing active connections on R7910...")
        cursor.execute(f"ALTER DATABASE {DATABASE} SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
        
        print(f"Dropping database {DATABASE}...")
        cursor.execute(f"DROP DATABASE {DATABASE}")
        
        print(f"Re-creating database {DATABASE}...")
        cursor.execute(f"CREATE DATABASE {DATABASE}")
        
        cursor.close()
        conn.close()
        
        # 3. Use SQLAlchemy to initialize the clean schema (now with variety, health_score, etc.)
        print("Re-initializing SQL tables on TheSharkEngine...")
        init_db()
        
        print("\nSUCCESS: R7910 Database reset with all new Architect columns.")
        
    except Exception as e:
        print(f"An error occurred during reset: {e}")

if __name__ == "__main__":
    force_reset_database()
