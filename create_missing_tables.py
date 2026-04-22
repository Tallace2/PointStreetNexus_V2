from database import init_db
from seed_inventory import seed_inventory

def patch_database():
    print("--- Patching Database with Missing Tables ---")
    init_db()
    print("Tables created. Seeding inventory...")
    seed_inventory()
    print("--- Patch Complete! ---")

if __name__ == "__main__":
    patch_database()
