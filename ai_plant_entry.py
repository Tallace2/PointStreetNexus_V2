import os
from database import SessionLocal
from models import BotanicalRegistry, MediaAsset, Planting, Project, Task
from datetime import datetime

def process_new_plant_photo(image_path, simulate=True):
    print(f"--- Processing Photo: {image_path} ---")
    
    db = SessionLocal()
    try:
        # 1. AI IDENTIFICATION (Simulation)
        ai_results = {
            "species": "Acer palmatum",
            "common_name": "Japanese Maple",
            "watering": "Regularly, keep soil moist",
            "sunlight": "Partial shade",
            "soil": "Well-drained",
        }

        # 2. PROJECT PICKER - List and Select Project
        projects = db.query(Project).all()
        print("\nAvailable Projects:")
        for idx, p in enumerate(projects):
            print(f"[{idx}] {p.name}")
        
        # In a real CLI we would take input, here we pick the first one
        selected_project = projects[0] if projects else None
        print(f"Assigning to Project: {selected_project.name if selected_project else 'None'}")

        # 3. SYNC SPECIES REGISTRY
        species = db.query(BotanicalRegistry).filter(BotanicalRegistry.scientific_name == ai_results["species"]).first()
        if not species:
            species = BotanicalRegistry(
                common_name=ai_results["common_name"],
                scientific_name=ai_results["species"],
                preferred_watering=ai_results["watering"],
                preferred_sunlight=ai_results["sunlight"]
            )
            db.add(species)
            db.flush()

        # 4. CREATE PLANTING & LINK PROJECT
        new_plant = Planting(
            species_id=species.species_id,
            plant_name=f"{ai_results['common_name']} Intake",
            status="In Quarantine",
            health_score=100
        )
        db.add(new_plant)
        db.flush()

        # 5. LOG PHOTO
        photo = MediaAsset(file_path=image_path, entity_type="Planting", entity_id=new_plant.planting_id)
        db.add(photo)

        db.commit()
        print(f"\nSUCCESS: {ai_results['common_name']} added and linked to {selected_project.name}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

def add_brainstorm_idea(idea_text):
    db = SessionLocal()
    try:
        new_task = Task(
            name=f"Brainstorm: {idea_text}",
            task_type="Brainstorm",
            priority=3,
            is_completed=False
        )
        db.add(new_task)
        db.commit()
        print(f"\nIdea saved to Brainstorm list: {idea_text}")
    finally:
        db.close()

if __name__ == "__main__":
    # 1. Process a new plant
    process_new_plant_photo("C:/Users/toddw/Pictures/Intake/Maple_01.JPG")
    
    # 2. Save brainstorm idea
    add_brainstorm_idea("Ray-Ban Meta Gen 2 glasses for hands-free property scanning/logging")
