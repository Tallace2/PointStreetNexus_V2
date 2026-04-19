from database import SessionLocal, init_db
from models import (GardenBed, SensorNode, SensorReading, Planting, WateringSchedule, 
                   Manufacturer, PartMaster, Project, IoTHub, IoTDevice, PLCNode, PLCTag,
                   Contact, Supplier, ProjectBOM, Task, PropertyGridNode)
from datetime import datetime, time, timedelta

def seed_data():
    # Ensure tables exist in SQL Server
    init_db()
    
    db = SessionLocal()
    try:
        # 1. Seed Contacts & Supply Chain
        john = Contact(name="John Doe", role="Supplier Rep", email="john@agrisupply.com", company_name="AgriSupply Co")
        db.add(john)
        db.flush()

        fox_farm = Manufacturer(name="FoxFarm", website="https://foxfarm.com")
        db.add(fox_farm)
        db.flush()

        agri_supply = Supplier(name="AgriSupply Local", website="https://agrisupply.com", contact_id=john.contact_id)
        db.add(agri_supply)
        db.flush()

        # 2. Seed Master Parts
        soil = PartMaster(name="Ocean Forest Soil", mfg_id=fox_farm.mfg_id, category="Soil", unit_cost=25.99, description="High-quality potting soil")
        nutes = PartMaster(name="Big Bloom Nutrient", mfg_id=fox_farm.mfg_id, category="Nutrient", unit_cost=18.50)
        solenoid = PartMaster(name="12V Water Solenoid", category="Irrigation", unit_cost=12.00)
        db.add_all([soil, nutes, solenoid])
        db.flush()

        # 3. Seed Projects & BOM/Tasks
        proj = Project(name="Spring 2024 Garden Expansion", status="Active", budget=1500.0, start_date=datetime.now())
        db.add(proj)
        db.flush()

        bom_item = ProjectBOM(project_id=proj.project_id, part_id=soil.part_id, quantity_required=10)
        task1 = Task(project_id=proj.project_id, name="Install RB-1 to RB-6", priority=1, task_type="To-Do")
        task2 = Task(project_id=proj.project_id, name="Configure Hubitat Marina Hub", priority=2, task_type="To-Do")
        db.add_all([bom_item, task1, task2])

        # 4. Seed Property Grid (Partial 10x20 sample)
        grid_nodes = []
        for x in range(1, 3):
            for y in range(1, 3):
                grid_nodes.append(PropertyGridNode(grid_x=x, grid_y=y, elevation=100.5 + (x*0.1), lidar_intensity=0.85, scan_device="iPhone 17 Pro Max"))
        db.add_all(grid_nodes)
        db.flush()

        # 5. Seed IoT Hubs
        home_hub = IoTHub(name="Hubitat C-8-Pro (Home)", ip_address="192.168.1.100")
        marina_hub = IoTHub(name="Hubitat C-8 (Marina)", ip_address="192.168.1.101")
        db.add_all([home_hub, marina_hub])
        db.flush()

        # 6. Seed PLC & Tags
        plc = PLCNode(name="Main Irrigation PLC", ip_address="192.168.1.200")
        db.add(plc)
        db.flush()

        tags = [PLCTag(plc_id=plc.plc_id, tag_name=f"RB{i}_Solenoid_Cmd", data_type="BOOL") for i in range(1, 7)]
        db.add_all(tags)

        # 7. Seed Hubitat Devices
        # Need to create the device first so SensorNode can reference it
        moisture_dev = IoTDevice(device_id="HUB-MOIST-001", hub_id=home_hub.hub_id, name="RB1 Moisture Sensor", device_type="Moisture Sensor")
        db.add(moisture_dev)
        db.flush()

        # 8. Seed Garden Beds & Link to Grid
        beds = []
        for i in range(1, 7):
            beds.append(GardenBed(name=f"RB-{i}", bed_type="Raised Bed", dimensions="3x15", soil_type="FoxFarm Ocean Forest", grid_node_id=grid_nodes[0].node_id))
        for i in range(1, 4):
            beds.append(GardenBed(name=f"Tote-{i}", bed_type="Tote", dimensions="2x2", soil_type="Potting Mix"))
        db.add_all(beds)
        db.flush()

        # 9. Seed Sensor Nodes
        # IMPORTANT: This must be added BEFORE the SensorReading to avoid IntegrityError
        s_node = SensorNode(sensor_id="SSMS-G2-RB1", iot_device_id=moisture_dev.device_id, bed_id=beds[0].bed_id)
        db.add(s_node)
        db.flush()

        # 10. Seed Plantings & Sensor Data
        p1 = Planting(bed_id=beds[0].bed_id, plant_name="Tomato", variety="Beefsteak", status="Active", health_score=95)
        db.add(p1)
        db.flush()

        reading = SensorReading(sensor_id=s_node.sensor_id, soil_moisture=32.5, temperature=74.0)
        db.add(reading)

        # 11. Seed Watering Schedule
        sched = WateringSchedule(planting_id=p1.planting_id, start_time=time(6, 0), duration_minutes=15)
        db.add(sched)

        db.commit()
        print("Comprehensive seed data applied successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
