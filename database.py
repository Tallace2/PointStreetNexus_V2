from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import urllib

# SQL Server Configuration
SERVER = 'localhost\\SQLEXPRESS'
DATABASE = 'PointStreetNexusDB'

# Connection string for Windows Authentication (Most reliable for local)
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

# Encode the connection string for SQLAlchemy
params = urllib.parse.quote_plus(connection_string)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database connection successful and tables verified.")

if __name__ == "__main__":
    init_db()
