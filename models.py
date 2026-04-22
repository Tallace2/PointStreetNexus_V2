from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text, LargeBinary, Time
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, UTC

class Base(DeclarativeBase):
    pass

# --- SYSTEM & ADMINISTRATION ---
class SystemGlossary(Base):
    __tablename__ = "System_Glossary"
    term_id = Column(Integer, primary_key=True)
    acronym = Column(String(20))
    term = Column(String(100), nullable=False)
    definition = Column(Text)
    created_at = Column(DateTime, default=datetime.now(UTC))

# --- INVENTORY: SUPPLIES, FERTILIZERS, PRODUCTS ---
class InventoryItem(Base):
    __tablename__ = "Inventory_Items"
    item_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50)) 
    type = Column(String(50)) 
    quantity = Column(Float)
    unit = Column(String(20)) 
    location = Column(String(100)) 
    purchase_date = Column(DateTime)
    expiration_date = Column(DateTime)
    supplier_id = Column(Integer, ForeignKey("Suppliers.supplier_id"), nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

# --- IT & INFRASTRUCTURE ---
class ITAsset(Base):
    __tablename__ = "IT_Assets"
    asset_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50)) 
    model = Column(String(100))
    ip_address = Column(String(50))
    mac_address = Column(String(50))
    location = Column(String(100))
    status = Column(String(20)) 
    purchase_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now(UTC))

class SoftwareAsset(Base):
    __tablename__ = "Software_Assets"
    software_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    version = Column(String(50))
    license_key = Column(String(200))
    installed_on = Column(Integer, ForeignKey("IT_Assets.asset_id"))
    vendor = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(UTC))

# --- CONTACTS & SUPPLY CHAIN ---
class Contact(Base):
    __tablename__ = "Contacts"
    contact_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    company_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(UTC))

class Manufacturer(Base):
    __tablename__ = "Manufacturers"
    mfg_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    website = Column(String(200))
    created_at = Column(DateTime, default=datetime.now(UTC))

class Supplier(Base):
    __tablename__ = "Suppliers"
    supplier_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    website = Column(String(200))
    contact_id = Column(Integer, ForeignKey("Contacts.contact_id"))
    created_at = Column(DateTime, default=datetime.now(UTC))

# --- MASTER PARTS & PROCUREMENT ---
class PartMaster(Base):
    __tablename__ = "Part_Master"
    part_id = Column(Integer, primary_key=True)
    part_number = Column(String(100))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    mfg_id = Column(Integer, ForeignKey("Manufacturers.mfg_id"))
    category = Column(String(50))
    unit_cost = Column(Float)
    created_at = Column(DateTime, default=datetime.now(UTC))

class Quote(Base):
    __tablename__ = "Quotes"
    quote_id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("Suppliers.supplier_id"))
    part_id = Column(Integer, ForeignKey("Part_Master.part_id"))
    quoted_price = Column(Float)
    quote_date = Column(DateTime, default=datetime.now(UTC))
    created_at = Column(DateTime, default=datetime.now(UTC))

class Order(Base):
    __tablename__ = "Orders"
    order_id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("Suppliers.supplier_id"))
    order_date = Column(DateTime, default=datetime.now(UTC))
    total_amount = Column(Float)
    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.now(UTC))

class OrderDetail(Base):
    __tablename__ = "Order_Details"
    detail_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("Orders.order_id"))
    part_id = Column(Integer, ForeignKey("Part_Master.part_id"))
    quantity = Column(Float)
    price_at_order = Column(Float)

# --- PROJECT MANAGEMENT ---
class Project(Base):
    __tablename__ = "Projects"
    project_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    budget = Column(Float)
    start_date = Column(DateTime)
    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.now(UTC))

class ProjectBOM(Base):
    __tablename__ = "Project_BOM"
    bom_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("Projects.project_id"))
    part_id = Column(Integer, ForeignKey("Part_Master.part_id"))
    quantity_required = Column(Float)
    created_at = Column(DateTime, default=datetime.now(UTC))

class Task(Base):
    __tablename__ = "Tasks"
    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("Projects.project_id"), nullable=True)
    name = Column(String(100), nullable=False)
    due_date = Column(DateTime)
    priority = Column(Integer)
    is_completed = Column(Boolean, default=False)
    task_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

# --- PROPERTY GRID & ZONES ---
class PropertyGridNode(Base):
    __tablename__ = "Property_Grid"
    node_id = Column(Integer, primary_key=True)
    grid_x = Column(Integer)
    grid_y = Column(Integer)
    elevation = Column(Float)
    lidar_intensity = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    last_scan_date = Column(DateTime, default=datetime.now(UTC))
    scan_device = Column(String(100))

class PropertyZone(Base):
    __tablename__ = "Property_Zones"
    zone_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False) # e.g., Sunshine Garden, Todds Marina, Courtyard
    description = Column(Text)
    grid_node_id = Column(Integer, ForeignKey("Property_Grid.node_id"), nullable=True) # Anchor point for the whole zone
    created_at = Column(DateTime, default=datetime.now(UTC))

# --- IOT & AUTOMATION ---
class IoTHub(Base):
    __tablename__ = "IoT_Hubs"
    hub_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ip_address = Column(String(50))
    api_key = Column(String(100))
    model = Column(String(50))
    created_at = Column(DateTime, default=datetime.now(UTC))

class PLCNode(Base):
    __tablename__ = "PLC_Nodes"
    plc_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.now(UTC))

class PLCTag(Base):
    __tablename__ = "PLC_Tags"
    tag_id = Column(Integer, primary_key=True)
    plc_id = Column(Integer, ForeignKey("PLC_Nodes.plc_id"))
    tag_name = Column(String(100))
    data_type = Column(String(20))
    description = Column(String(200))
    created_at = Column(DateTime, default=datetime.now(UTC))

class IoTDevice(Base):
    __tablename__ = "IoT_Devices"
    device_id = Column(String(100), primary_key=True)
    hub_id = Column(Integer, ForeignKey("IoT_Hubs.hub_id"))
    name = Column(String(100))
    device_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.now(UTC))

class SensorNode(Base):
    __tablename__ = "Sensor_Nodes"
    sensor_id = Column(String(100), primary_key=True)
    iot_device_id = Column(String(100), ForeignKey("IoT_Devices.device_id"))
    zone_id = Column(Integer, ForeignKey("Property_Zones.zone_id"), nullable=True)
    bed_id = Column(Integer, ForeignKey("Garden_Beds.bed_id"), nullable=True)

# --- GARDEN & BIOLOGICALS ---
class GardenBed(Base):
    __tablename__ = "Garden_Beds"
    bed_id = Column(Integer, primary_key=True)
    zone_id = Column(Integer, ForeignKey("Property_Zones.zone_id"), nullable=True) # Linked to a Zone
    name = Column(String(50)) # e.g., Camilia Bed, Garage Planter, RB-1
    bed_type = Column(String(50)) # Raised Bed, Container, Trench, Row, Ground
    dimensions = Column(String(50))
    soil_type = Column(String(100))
    grid_node_id = Column(Integer, ForeignKey("Property_Grid.node_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC))

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
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

class Planting(Base):
    __tablename__ = "Plantings"
    planting_id = Column(Integer, primary_key=True)
    bed_id = Column(Integer, ForeignKey("Garden_Beds.bed_id"), nullable=True)
    species_id = Column(Integer, ForeignKey("Botanical_Registry.species_id"), nullable=True)
    plant_name = Column(String(100))
    variety = Column(String(100))
    status = Column(String(50))
    health_score = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    date_planted = Column(DateTime, default=datetime.now(UTC))
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

# --- HISTORIAN LOGS (The Time Machine) ---
class SensorReading(Base):
    __tablename__ = "Sensor_Readings"
    reading_id = Column(Integer, primary_key=True)
    sensor_id = Column(String(100), ForeignKey("Sensor_Nodes.sensor_id"))
    timestamp = Column(DateTime, default=datetime.now(UTC))
    soil_moisture = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float) # Added humidity
    lux = Column(Float) # Added light levels

class IrrigationLog(Base):
    __tablename__ = "Irrigation_Logs"
    log_id = Column(Integer, primary_key=True)
    zone_id = Column(Integer, ForeignKey("Property_Zones.zone_id"), nullable=True)
    bed_id = Column(Integer, ForeignKey("Garden_Beds.bed_id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.now(UTC))
    duration_minutes = Column(Float)
    gallons_used = Column(Float)
    trigger_source = Column(String(50)) # e.g., 'PLC Auto', 'Manual Hubitat', 'App Override'

class PlantHealthLog(Base):
    __tablename__ = "Plant_Health_Logs"
    log_id = Column(Integer, primary_key=True)
    planting_id = Column(Integer, ForeignKey("Plantings.planting_id"))
    timestamp = Column(DateTime, default=datetime.now(UTC))
    health_score = Column(Integer)
    observation = Column(Text) # e.g., "Found aphids", "Showing new buds"
    treatment_applied = Column(String(100)) # Linked to Inventory later

class WateringSchedule(Base):
    __tablename__ = "Watering_Schedules"
    schedule_id = Column(Integer, primary_key=True)
    planting_id = Column(Integer, ForeignKey("Plantings.planting_id"))
    start_time = Column(Time)
    duration_minutes = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(UTC))

class MediaAsset(Base):
    __tablename__ = "Media_Assets"
    media_id = Column(Integer, primary_key=True)
    file_path = Column(String(500))
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now(UTC))
    ai_confidence = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
