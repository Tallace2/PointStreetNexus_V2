from database import SessionLocal, init_db
from models import (PropertyZone, GardenBed, SensorNode, SensorReading, Planting, WateringSchedule, 
                   Manufacturer, PartMaster, Project, IoTHub, IoTDevice, PLCNode, PLCTag,
                   Contact, Supplier, ProjectBOM, Task, PropertyGridNode, SystemGlossary)
from datetime import datetime, time, timedelta, UTC

def seed_data():
    init_db()
    db = SessionLocal()
    try:
        # 1. Seed System Glossary (Expanded Categories)
        glossary = [
            SystemGlossary(acronym="SG", term="Sunshine Garden", definition="The large 30x100 garden area on the east side."),
            SystemGlossary(acronym="TM", term="Todds Marina", definition="The dock and boat slip area."),
            SystemGlossary(acronym="RB", term="Raised Bed", definition="Wooden planter boxes with customized soil mixes."),
            SystemGlossary(acronym="CY", term="Courtyard", definition="Enclosed seating area between the house and garage."),
            SystemGlossary(acronym="PLC", term="Programmable Logic Controller", definition="Allen-Bradley L32E running the irrigation valves."),
            SystemGlossary(acronym="EC", term="Electrical Conductivity", definition="Measure of nutrient salts in the soil/water solution."),
            SystemGlossary(acronym="pH", term="Potential of Hydrogen", definition="Measure of soil acidity/alkalinity. Most plants prefer 6.0-7.0."),
            SystemGlossary(acronym="N-P-K", term="Nitrogen-Phosphorus-Potassium", definition="The three primary macronutrients in fertilizer (e.g., 10-10-10)."),
            SystemGlossary(acronym="Tip", term="Master Gardener Tip: Watering", definition="Water deeply and infrequently to encourage deep root growth, rather than shallow, frequent watering.")
        ]
        db.add_all(glossary)

        # 2. Seed Property Zones
        zones = [
            PropertyZone(name="Sunshine Garden", description="Primary 30x100 planting area under the trees."),
            PropertyZone(name="Courtyard", description="Central paved area with container plants, hanging baskets, and work table."),
            PropertyZone(name="Deck", description="Back deck overlooking the lake."),
            PropertyZone(name="North Property Line", description="Border area containing the Camilia beds."),
            PropertyZone(name="Todds Marina", description="Lakeside infrastructure and dock planters.")
        ]
        db.add_all(zones)
        db.flush()

        # 3. Seed Property Grid (Partial 10x20 sample)
        grid_nodes = []
        for x in range(1, 3):
            for y in range(1, 3):
                grid_nodes.append(PropertyGridNode(grid_x=x, grid_y=y, elevation=100.5 + (x*0.1), lidar_intensity=0.85, scan_device="iPhone 17 Pro Max"))
        db.add_all(grid_nodes)
        db.flush()

        # 4. Seed IoT Hubs & PLCs
        home_hub = IoTHub(name="Hubitat C-8-Pro (Home)", ip_address="192.168.1.100")
        plc = PLCNode(name="Main Irrigation PLC", ip_address="192.168.1.200")
        db.add_all([home_hub, plc])
        db.flush()

        # Define PLC Tags for Handshake Architecture
        tags = [
            PLCTag(plc_id=plc.plc_id, tag_name="PC_to_PLC_Heartbeat", data_type="BOOL", description="Watchdog toggle from Python"),
            PLCTag(plc_id=plc.plc_id, tag_name="PLC_to_PC_Heartbeat", data_type="BOOL", description="Watchdog echo from PLC"),
            PLCTag(plc_id=plc.plc_id, tag_name="Zone_1_Cmd", data_type="BOOL", description="Command to open Valve 1"),
            PLCTag(plc_id=plc.plc_id, tag_name="Zone_1_Duration_Min", data_type="DINT", description="Requested duration in minutes"),
            PLCTag(plc_id=plc.plc_id, tag_name="Zone_1_Status", data_type="DINT", description="0=Ready, 1=Watering, 2=Done, 9=Error")
        ]
        db.add_all(tags)

        moisture_dev = IoTDevice(device_id="HUB-MOIST-001", hub_id=home_hub.hub_id, name="SG Master Moisture", device_type="Moisture Sensor")
        db.add(moisture_dev)
        db.flush()

        # 5. Seed Specific Beds/Planters into Zones (Including Courtyard details)
        sg_zone = next(z for z in zones if z.name == "Sunshine Garden")
        north_zone = next(z for z in zones if z.name == "North Property Line")
        deck_zone = next(z for z in zones if z.name == "Deck")
        cy_zone = next(z for z in zones if z.name == "Courtyard")

        beds = [
            GardenBed(zone_id=sg_zone.zone_id, name="RB-1", bed_type="Raised Bed", soil_type="FoxFarm Mix"),
            GardenBed(zone_id=sg_zone.zone_id, name="Zoned Bed A", bed_type="Ground", soil_type="Native Soil"),
            GardenBed(zone_id=north_zone.zone_id, name="Camilia Bed", bed_type="Trench", dimensions="5x30"),
            GardenBed(zone_id=deck_zone.zone_id, name="Deck Container 1", bed_type="Container"),
            GardenBed(name="Big Garage Planter", bed_type="Container", dimensions="4x4"),
            
            # Courtyard additions
            GardenBed(zone_id=cy_zone.zone_id, name="CY Hanging Baskets (5)", bed_type="Container"),
            GardenBed(zone_id=cy_zone.zone_id, name="CY Medium Containers (6)", bed_type="Container"),
            GardenBed(zone_id=cy_zone.zone_id, name="CY Misc Pots", bed_type="Container"),
            GardenBed(zone_id=cy_zone.zone_id, name="CY Work Table (Infant Plants)", bed_type="Propagation Station")
        ]
        db.add_all(beds)
        db.flush()

        # 6. Seed Sensor Nodes
        s_node = SensorNode(sensor_id="SSMS-G2-SG1", iot_device_id=moisture_dev.device_id, zone_id=sg_zone.zone_id)
        db.add(s_node)
        db.flush()

        # Including new sensor reading types
        reading = SensorReading(sensor_id=s_node.sensor_id, soil_moisture=32.5, temperature=74.0, humidity=55.0, lux=8000)
        db.add(reading)

        db.commit()
        print("V3 Enterprise seed data applied successfully!")
        
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
