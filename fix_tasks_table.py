import pyodbc
from database import SERVER, DATABASE, USERNAME, PASSWORD

def fix_tasks_table():
    print(f"--- Fixing Tasks Table Schema on {SERVER} ---")
    
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    
    try:
        conn = pyodbc.connect(connection_string, autocommit=True)
        cursor = conn.cursor()
        
        # Check if created_at column exists
        cursor.execute(f"SELECT COL_LENGTH('Tasks', 'created_at')")
        col_exists = cursor.fetchone()[0]
        
        if not col_exists:
            print("Adding 'created_at' column to Tasks table...")
            cursor.execute("ALTER TABLE Tasks ADD created_at DATETIME")
            print("Column added successfully.")
        else:
            print("'created_at' column already exists.")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error updating Tasks table: {e}")

if __name__ == "__main__":
    fix_tasks_table()
