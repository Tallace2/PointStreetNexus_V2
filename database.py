from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import urllib

# SERVER configuration for TheSharkEngine
SERVER = '192.168.1.245,55658' 
DATABASE = 'PointStreetNexusDB'
USERNAME = 'sa'
PASSWORD = 'Bailey9751'

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate=yes;"
    f"Connection Timeout=60;"
)

params = urllib.parse.quote_plus(connection_string)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Create engine for R7910
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # This rebuilds the tables ON THE SHARK ENGINE
    Base.metadata.create_all(bind=engine)
    print(f"SQL COMMAND SENT: Tables synchronized on TheSharkEngine (192.168.1.245).")

if __name__ == "__main__":
    init_db()
