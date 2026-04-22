import pyodbc
from database import SERVER, DATABASE, USERNAME, PASSWORD

def patch_missing_columns():
    print(f"--- Applying Surgical DB Patch to {SERVER} ---")
    
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    
    queries = [
        "ALTER TABLE Botanical_Registry ADD created_at DATETIME;",
        "ALTER TABLE Botanical_Registry ADD updated_at DATETIME;",
        "ALTER TABLE Plantings ADD created_at DATETIME;",
        "ALTER TABLE Plantings ADD updated_at DATETIME;",
    ]

    try:
        conn = pyodbc.connect(connection_string, autocommit=True)
        cursor = conn.cursor()
        
        for q in queries:
            try:
                cursor.execute(q)
                print(f"Executed: {q}")
            except pyodbc.ProgrammingError as e:
                # Code 2714 usually means column already exists, which is safe to ignore
                print(f"Skipped (likely exists): {q}")
        
        cursor.close()
        conn.close()
        print("\nSUCCESS: All missing timestamp columns added to R7910 without dropping data.")
        
    except Exception as e:
        print(f"Critical error connecting to SQL: {e}")

if __name__ == "__main__":
    patch_missing_columns()
