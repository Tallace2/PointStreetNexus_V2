from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text, LargeBinary, Time
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

# --- CONTACTS & SUPPLY CHAIN ---
class Contact(Base):
    __tablename__ = "Contacts"
    contact_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    company_name = Column(String(100))

class Manufacturer(Base):
    __tablename__ = "Manufacturers"
    mfg_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    website = Column(String(200))

class Supplier(Base):
    __tablename__ = "Suppliers"
    supplier_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    website = Column(String(200))
    contact_id = Column(Integer, ForeignKey("Contacts.contact_id"))

# --- MASTER PARTS ---
class PartMaster(Base):
    __tablename__ = "Part_Master"
    part_id = Column(Integer, primary_key=True)
    part_number = Column(String(100))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    mfg_id = Column(Integer, ForeignKey("Manufacturers.mfg_id"))
    category = Column(String(50))
    unit_cost = Column(Float)

# --- PROJECT MANAGEMENT ---
class Project(Base):
    __tablename__ = "Projects"
    project_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    budget = Column(Float)
    start_date = Column(DateTime) # Restoring start_date
    status = Column(String(20))

class ProjectBOM(Base):
    __tablename__ = "Project_BOM"
    bom_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("Projects.project_id"))
    part_id = Column(Integer, ForeignKey("Part_Master.part_id"))
    quantity_required = Column(Float)

class Task(Base):
    __tablename__ = "Tasks"
    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("Projects.project_id"), nullable=True)
    name = Column(String(100), nullable=False)
    due_date = Column(DateTime)
    priority = Column(Integer)
    is_completed = Column(Boolean, default=False)
    task_type = Column(String(50))

# --- PROPERTY GRID ---
class PropertyGridNode(Base):
    __tablename__ = "Property_Grid"
    node_id = Column(Integer, primary_key=True)
    grid_x = Column(Integer)
    grid_y = Column(Integer)
    elevation = Column(Float)
    lidar_intensity = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    last_scan_date = Column(DateTime, default=datetime.utcnow)

# --- IOT & AUTOMATION ---
class IoTHub(Base):
    __tablename__ = "IoT_Hubs"
    hub_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ip_address = Column(String(50))
    api_key = Column(String(100))
    model = Column(String(50))

class PLCNode(Base):
    __tablename__ = "PLC_Nodes"
    plc_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ip_address = Column(String(50))

class PLCTag(Base):
    __tablename__ = "PLC_Tags"
    tag_id = Column(Integer, primary_key=True)
    plc_id = Column(Integer, ForeignKey("PLC_Nodes.plc_id"))
    tag_name = Column(String(100))
    data_type = Column(String(20))
    description = Column(String(200))

class IoTDevice(Base):
    __tablename__ = "IoT_Devices"
    device_id = Column(String(100), primary_key=True)
    hub_id = Column(Integer, ForeignKey("IoT_Hubs.hub_id"))
    name = Column(String(100))

class SensorNode(Base):
    __tablename__ = "Sensor_Nodes"
    sensor_id = Column(String(100), primary_key=True)
    iot_device_id = Column(String(100), ForeignKey("IoT_Devices.device_id"))
    bed_id = Column(Integer, ForeignKey("Garden_Beds.bed_id"), nullable=True)

# --- GARDEN & BIOLOGICALS ---
class GardenBed(Base):
    __tablename__ = "Garden_Beds"
    bed_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    bed_type = Column(String(50))
    dimensions = Column(String(50))
    soil_type = Column(String(100))

class BotanicalRegistry(Base):
    __tablename__ = "Botanical_Registry"
    species_id = Column(Integer, primary_key=True)
    common_name = Column(String(100), nullable=False)
    scientific_name = Column(String(100))
    plant_category = Column(String(50))
    indoor_outdoor = Column(String(50))
    description = Column(Text)
    preferred_watering = Column(String(200))
    watering_frequency_days = Column(Integer)
    preferred_sunlight = Column(String(100))
    preferred_soil = Column(String(200))
    fertilizer_needs = Column(String(200))
    growth_rate = Column(String(50))
    hardiness_zones = Column(String(100))
    notes = Column(Text)
    ai_confidence = Column(Float)

class Planting(Base):
    __tablename__ = "Plantings"
    planting_id = Column(Integer, primary_key=True)
    bed_id = Column(Integer, ForeignKey("Garden_Beds.bed_id"), nullable=True)
    species_id = Column(Integer, ForeignKey("Botanical_Registry.species_id"), nullable=True)
    plant_name = Column(String(100))
    status = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    date_planted = Column(DateTime, default=datetime.utcnow)

class SensorReading(Base):
    __tablename__ = "Sensor_Readings"
    reading_id = Column(Integer, primary_key=True)
    sensor_id = Column(String(100), ForeignKey("Sensor_Nodes.sensor_id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    soil_moisture = Column(Float)
    temperature = Column(Float)

class WateringSchedule(Base):
    __tablename__ = "Watering_Schedules"
    schedule_id = Column(Integer, primary_key=True)
    planting_id = Column(Integer, ForeignKey("Plantings.planting_id"))
    start_time = Column(Time)
    duration_minutes = Column(Integer)
    is_active = Column(Boolean, default=True)

class MediaAsset(Base):
    __tablename__ = "Media_Assets"
    media_id = Column(Integer, primary_key=True)
    file_path = Column(String(500))
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ai_confidence = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
