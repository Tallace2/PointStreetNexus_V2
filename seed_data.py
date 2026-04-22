from database import SessionLocal, init_db
from models import (PropertyZone, GardenBed, SensorNode, SensorReading, Planting, WateringSchedule, 
                   Manufacturer, PartMaster, Project, IoTHub, IoTDevice, PLCNode, PLCTag,
                   Contact, Supplier, ProjectBOM, Task, PropertyGridNode, SystemGlossary)
from datetime import datetime, time, timedelta, UTC

def seed_data():
    init_db()
    db = SessionLocal()
    print("--- Seeding Core Infrastructure & Glossary ---")
    try:
        # 1. Seed System Glossary (Expanded Categories)
        glossary_terms = [
            ("SG", "Sunshine Garden", "The large 30x100 garden area on the east side."),
            ("TM", "Todds Marina", "The dock and boat slip area."),
            ("RB", "Raised Bed", "Wooden planter boxes with customized soil mixes."),
            ("CY", "Courtyard", "Enclosed seating area between the house and garage."),
            ("PLC", "Programmable Logic Controller", "Allen-Bradley L32E running the irrigation valves."),
            ("EC", "Electrical Conductivity", "Measure of nutrient salts in the soil/water solution."),
            ("pH", "Potential of Hydrogen", "Measure of soil acidity/alkalinity. Most plants prefer 6.0-7.0."),
            ("N-P-K", "Nitrogen-Phosphorus-Potassium", "The three primary macronutrients in fertilizer (e.g., 10-10-10)."),
            ("Tip", "Master Gardener Tip: Watering", "Water deeply and infrequently to encourage deep root growth.")
        ]
        
        for ac, term, defn in glossary_terms:
            if not db.query(SystemGlossary).filter_by(acronym=ac).first():
                db.add(SystemGlossary(acronym=ac, term=term, definition=defn))
        db.commit()

        # 2. Seed Property Zones
        zone_data = [
            ("Sunshine Garden", "Primary 30x100 planting area under the trees."),
            ("Courtyard", "Central paved area with container plants, hanging baskets, and work table."),
            ("Deck", "Back deck overlooking the lake."),
            ("North Property Line", "Border area containing the Camilia beds."),
            ("Todds Marina", "Lakeside infrastructure and dock planters.")
        ]
        zones = {}
        for name, desc in zone_data:
            zone = db.query(PropertyZone).filter_by(name=name).first()
            if not zone:
                zone = PropertyZone(name=name, description=desc)
                db.add(zone)
                db.commit()
                db.refresh(zone)
            zones[name] = zone

        # 3. Seed Property Grid (10x20 Nano 300 Simulation)
        # Check if grid exists
        if db.query(PropertyGridNode).count() == 0:
            print("Seeding Property Grid...")
            grid_nodes = []
            for x in range(1, 11):
                for y in range(1, 21):
                    # Simulate a sloping terrain towards the lake
                    elevation = 105.0 - (y * 0.2) + (x * 0.05) 
                    grid_nodes.append(PropertyGridNode(grid_x=x, grid_y=y, elevation=elevation, lidar_intensity=0.85, scan_device="Nano 300 Sim"))
            db.add_all(grid_nodes)
            db.commit()

        # 4. Seed IoT Hubs & PLCs
        if not db.query(IoTHub).filter_by(ip_address="192.168.1.100").first():
            home_hub = IoTHub(name="Hubitat C-8-Pro (Home)", ip_address="192.168.1.100")
            db.add(home_hub)
            db.commit()

        plc = db.query(PLCNode).filter_by(ip_address="192.168.1.200").first()
        if not plc:
            plc = PLCNode(name="Main Irrigation PLC", ip_address="192.168.1.200")
            db.add(plc)
            db.commit()
            db.refresh(plc)
            
            tags = [
                PLCTag(plc_id=plc.plc_id, tag_name="PC_to_PLC_Heartbeat", data_type="BOOL", description="Watchdog toggle from Python"),
                PLCTag(plc_id=plc.plc_id, tag_name="PLC_to_PC_Heartbeat", data_type="BOOL", description="Watchdog echo from PLC"),
                PLCTag(plc_id=plc.plc_id, tag_name="Zone_1_Cmd", data_type="BOOL", description="Command to open Valve 1"),
                PLCTag(plc_id=plc.plc_id, tag_name="Zone_1_Duration_Min", data_type="DINT", description="Requested duration in minutes"),
                PLCTag(plc_id=plc.plc_id, tag_name="Zone_1_Status", data_type="DINT", description="0=Ready, 1=Watering, 2=Done, 9=Error")
            ]
            db.add_all(tags)
            db.commit()

        # 5. Seed Specific Beds/Planters into Zones
        bed_data = [
            (zones["Sunshine Garden"].zone_id, "RB-1", "Raised Bed", "FoxFarm Mix", "3x15"),
            (zones["Sunshine Garden"].zone_id, "Zoned Bed A", "Ground", "Native Soil", "10x10"),
            (zones["North Property Line"].zone_id, "Camilia Bed", "Trench", "Acidic Mix", "5x30"),
            (zones["Deck"].zone_id, "Deck Container 1", "Container", "Potting Soil", "2x2"),
            (None, "Big Garage Planter", "Container", "Potting Soil", "4x4"),
            (zones["Courtyard"].zone_id, "CY Hanging Baskets (5)", "Container", "Moisture Control", "Hanging"),
            (zones["Courtyard"].zone_id, "CY Medium Containers (6)", "Container", "Potting Mix", "Medium"),
            (zones["Courtyard"].zone_id, "CY Misc Pots", "Container", "Various", "Small"),
            (zones["Courtyard"].zone_id, "CY Work Table (Infant Plants)", "Propagation Station", "Seed Starter", "Table")
        ]
        
        for z_id, b_name, b_type, s_type, dims in bed_data:
            if not db.query(GardenBed).filter_by(name=b_name).first():
                db.add(GardenBed(zone_id=z_id, name=b_name, bed_type=b_type, soil_type=s_type, dimensions=dims))
        db.commit()

        print("V3 Enterprise core data applied successfully!")
        
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
