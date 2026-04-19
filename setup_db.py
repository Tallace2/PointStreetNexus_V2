import pyodbc

# SQL Server Configuration
SERVER = 'localhost\\SQLEXPRESS'

def create_database():
    # Connect to the 'master' database to perform administrative tasks
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE=master;"
        f"Trusted_Connection=yes;"
    )
    
    try:
        # Use autocommit=True so we can run CREATE DATABASE
        conn = pyodbc.connect(connection_string, autocommit=True)
        cursor = conn.cursor()
        
        # Check if database already exists
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'PointStreetNexusDB'")
        if cursor.fetchone():
            print("Database 'PointStreetNexusDB' already exists.")
        else:
            print("Creating database 'PointStreetNexusDB'...")
            cursor.execute("CREATE DATABASE PointStreetNexusDB")
            print("Database created successfully.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nTroubleshooting tips:")
        print(f"1. Ensure your SQL Server instance name is correct (currently: {SERVER})")
        print("2. Ensure 'ODBC Driver 17 for SQL Server' is installed on your machine.")

if __name__ == "__main__":
    create_database()
