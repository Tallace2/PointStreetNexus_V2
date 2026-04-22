from database import SessionLocal
from models import InventoryItem, Planting, BotanicalRegistry
from datetime import datetime, UTC

def seed_inventory():
    print("--- Seeding Supply & Product Inventory ---")
    db = SessionLocal()
    
    try:
        # Inventory Items
        items = [
            InventoryItem(name="Planting Soil", category="Soil/Mix", type="Organic", quantity=5, unit="Bags", location="Garden Shed"),
            InventoryItem(name="Fertilizer 13-13-13", category="Fertilizer", type="Synthetic", quantity=10, unit="Lbs", location="Garden Shed"),
            InventoryItem(name="Garden Hoses", category="Tools/Equipment", type="N/A", quantity=3, unit="Items", location="Garage"),
            InventoryItem(name="Sprinklers", category="Tools/Equipment", type="N/A", quantity=4, unit="Items", location="Garage"),
            InventoryItem(name="Greenhouse Fans", category="Tools/Equipment", type="N/A", quantity=2, unit="Items", location="Greenhouse"),
            InventoryItem(name="Shovels", category="Tools/Equipment", type="N/A", quantity=2, unit="Items", location="Garden Shed"),
            InventoryItem(name="Rakes", category="Tools/Equipment", type="N/A", quantity=2, unit="Items", location="Garden Shed"),
            InventoryItem(name="Spade", category="Tools/Equipment", type="N/A", quantity=1, unit="Items", location="Garden Shed"),
            InventoryItem(name="Sledge Hammer", category="Tools/Equipment", type="N/A", quantity=1, unit="Items", location="Garage"),
            InventoryItem(name="Broom", category="Tools/Equipment", type="N/A", quantity=2, unit="Items", location="Garage"),
            InventoryItem(name="Plant Trays", category="Container", type="N/A", quantity=15, unit="Items", location="Greenhouse"),
            InventoryItem(name="Lava Rock", category="Additive", type="Natural", quantity=2, unit="Bags", location="Garden Shed"),
            InventoryItem(name="Rockwool Starter Pods", category="Propagation", type="Synthetic", quantity=50, unit="Items", location="Greenhouse"),
            InventoryItem(name="Assorted Containers/Pots", category="Container", type="N/A", quantity=30, unit="Items", location="Garden Shed"),
            InventoryItem(name="Master Seed Library", category="Seeds", type="Mixed", quantity=1, unit="Box", location="Office", notes="Contains assorted vegetable and flower seeds"),
            InventoryItem(name="Spray Bottles", category="Tools/Equipment", type="N/A", quantity=4, unit="Items", location="Greenhouse"),
            InventoryItem(name="Insecticidal Soap", category="Pest Control", type="Organic", quantity=1, unit="Gallons", location="Garden Shed"),
            InventoryItem(name="Irish Spring Soap", category="Pest Control", type="Homemade", quantity=6, unit="Bars", location="Garden Shed", notes="Deer/pest deterrent")
        ]
        
        # Check if already exists to prevent duplicate seeding
        existing_items = [i.name for i in db.query(InventoryItem).all()]
        new_items = [item for item in items if item.name not in existing_items]
        
        if new_items:
            db.add_all(new_items)
            db.commit()
            print(f"Successfully added {len(new_items)} new inventory items to SQL Server.")
        else:
            print("Inventory items already exist. Skipping duplicates.")

        # Pre-planting Inventory (Plants ready to be planted)
        # Create a generic registry entry for un-identified ready-to-plant inventory
        unidentified_spec = db.query(BotanicalRegistry).filter(BotanicalRegistry.scientific_name == "Unknown Species").first()
        if not unidentified_spec:
            unidentified_spec = BotanicalRegistry(common_name="Unidentified Seedling/Plant", scientific_name="Unknown Species", plant_category="Unknown")
            db.add(unidentified_spec)
            db.commit()
            db.refresh(unidentified_spec)
            
        ready_plants = [
            Planting(species_id=unidentified_spec.species_id, plant_name="Tomato Seedlings", status="Ready to Plant", date_planted=datetime.now(UTC)),
            Planting(species_id=unidentified_spec.species_id, plant_name="Pepper Starts", status="Ready to Plant", date_planted=datetime.now(UTC)),
            Planting(species_id=unidentified_spec.species_id, plant_name="Basil Clones", status="Ready to Plant", date_planted=datetime.now(UTC))
        ]
        
        db.add_all(ready_plants)
        db.commit()
        print("Successfully added ready-to-plant inventory to Plantings table.")

    except Exception as e:
        print(f"Error seeding inventory: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_inventory()
