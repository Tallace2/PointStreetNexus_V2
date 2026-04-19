import pyodbc
import os
import shutil
from database import init_db

# SQL Server Configuration
SERVER = 'localhost\\SQLEXPRESS'
DATABASE = 'PointStreetNexusDB'
MEDIA_DIR = "media"

def force_reset_database():
    print(f"--- Force Resetting Database and Media for {DATABASE} ---")
    
    # 1. Clear the local Media Folder
    if os.path.exists(MEDIA_DIR):
        print(f"Cleaning media folder: {MEDIA_DIR}")
        shutil.rmtree(MEDIA_DIR)
        os.makedirs(MEDIA_DIR)
    
    # 2. Connect to the 'master' database to drop the entire Nexus DB
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE=master;"
        f"Trusted_Connection=yes;"
    )
    
    try:
        conn = pyodbc.connect(connection_string, autocommit=True)
        cursor = conn.cursor()
        
        # Kill active connections
        print("Closing active database connections...")
        cursor.execute(f"ALTER DATABASE {DATABASE} SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
        
        # Drop and Recreate
        print(f"Dropping database {DATABASE}...")
        cursor.execute(f"DROP DATABASE {DATABASE}")
        
        print(f"Re-creating database {DATABASE}...")
        cursor.execute(f"CREATE DATABASE {DATABASE}")
        
        cursor.close()
        conn.close()
        
        # 3. Use SQLAlchemy to initialize the clean schema
        print("Re-initializing SQL tables...")
        init_db()
        
        print("\nSUCCESS: Database and Photos have been completely wiped and reset.")
        
    except Exception as e:
        print(f"An error occurred during reset: {e}")

if __name__ == "__main__":
    force_reset_database()
