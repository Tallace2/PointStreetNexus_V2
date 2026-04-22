import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from database import SessionLocal, engine, init_db, SERVER
from models import (Base, GardenBed, SensorReading, Planting, Task, BotanicalRegistry, 
                   IoTHub, PLCNode, PLCTag, Project, MediaAsset, PropertyGridNode,
                   ITAsset, SoftwareAsset, InventoryItem, PropertyZone, SystemGlossary,
                   IrrigationLog, PlantHealthLog)
from datetime import datetime, UTC, timedelta
import os
import requests
import base64
import shutil
import socket
from PIL import Image, ImageOps

# Version Configuration
VERSION = "V3.1 (UI Sprint 1)"

# Support for HEIC
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

# Import the lake data collector
from lake_collector import get_lake_data

# --- PAGE CONFIG ---
st.set_page_config(page_title=f"PSN Architect", layout="wide", initial_sidebar_state="expanded")

# --- UI THEME ---
st.markdown(f"""
    <style>
    .main {{ background-color: #f0f2f6; }}
    .stMetric {{ background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #d1d5db; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }}
    h1, h2, h3 {{ color: #003366; font-family: 'Segoe UI', sans-serif; }}
    .stButton>button {{ background-color: #003366; color: white; border-radius: 8px; height: 3em; }}
    /* Mobile Table Fix */
    .stDataFrame {{ overflow-x: auto; }}
    </style>
    """, unsafe_allow_html=True)

# --- DIRECTORY SETUP ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "02_Data")
MEDIA_DIR = os.path.join(DATA_DIR, "Media")

MEDIA_SUBDIRS = {
    "Plantings": os.path.join(MEDIA_DIR, "plantings"),
    "Property": os.path.join(MEDIA_DIR, "property_anchors"),
    "Lidar": os.path.join(MEDIA_DIR, "lidar_scans"),
    "Projects": os.path.join(MEDIA_DIR, "projects")
}

TEMP_DIR = os.path.join(BASE_DIR, "04_Temp")
QUEUE_DIR = os.path.join(TEMP_DIR, "intake_queue")
AUTO_DIR = os.path.join(BASE_DIR, "03_Automation")

for d in MEDIA_SUBDIRS.values(): os.makedirs(d, exist_ok=True)
os.makedirs(QUEUE_DIR, exist_ok=True)
os.makedirs(AUTO_DIR, exist_ok=True)

KEY_FILE = ".api_key"
if 'api_key' not in st.session_state:
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f: st.session_state['api_key'] = f.read().strip()
    else:
        st.session_state['api_key'] = ""

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try: s.connect(('8.8.8.8', 1)); IP = s.getsockname()[0]
    except: IP = '127.0.0.1'
    finally: s.close()
    return IP
LOCAL_IP = get_local_ip()

def identify_plant(image_bytes, simulate=False):
    if simulate:
        return {"scientific_name": "Acer palmatum", "common_name": "Mock Japanese Maple", "description": "Simulation mode active.", "plant_category": "Trees", "watering": "Medium", "watering_days": 4, "sunlight": "Partial Shade", "soil": "Well-drained", "fertilizer": "10-10-10", "growth_rate": "Moderate", "confidence": 0.99}
    key = st.session_state['api_key']
    if not key: return None
    b64 = base64.b64encode(image_bytes).decode("ascii")
    url = "https://api.plant.id/v2/identify"
    payload = {"api_key": key, "images": [b64], "modifiers": ["crops_fast"], "plant_details": ["common_names", "watering", "sunlight", "taxonomy", "description", "soil", "growth_rate"]}
    try:
        resp = requests.post(url, json=payload, timeout=20)
        data = resp.json()
        if data.get("suggestions"):
            best = data["suggestions"][0]
            det = best.get("plant_details", {})
            w = det.get("watering", {}).get("max", 2)
            return {"scientific_name": best.get("plant_name", "Unknown"), "common_name": det.get("common_names", ["Unknown"])[0] if det.get("common_names") else "Unknown", "description": det.get("description", {}).get("value", "No description."), "plant_category": det.get("taxonomy", {}).get("order", "Biological"), "watering": {1:"Low", 2:"Medium", 3:"High"}.get(w, "Medium"), "watering_days": det.get("watering", {}).get("min", 7), "sunlight": str(det.get("sunlight", {}).get("description", "Partial Sun")), "soil": str(det.get("soil", {}).get("description", "Well-Drained")), "fertilizer": "Monthly Standard", "growth_rate": det.get("growth_rate", "Moderate"), "confidence": float(best.get("probability", 0))}
    except: return None
    return None

def main():
    st.sidebar.title(f"🌿 PSN Architect {VERSION}")
    
    # --- SPRINT 1: CATEGORIZED NAVIGATION ---
    category = st.sidebar.selectbox("📂 Category", [
        "🌱 Horticulture", 
        "📦 Operations", 
        "🗺️ Spatial", 
        "📈 Analytics", 
        "⚙️ System"
    ])
    
    if category == "🌱 Horticulture":
        menu = st.sidebar.radio("Navigation", ["Executive Dashboard", "Species Registry", "Garden Inventory", "Intake Center", "Media Asset CRUD"])
    elif category == "📦 Operations":
        menu = st.sidebar.radio("Navigation", ["Supply Inventory", "Projects & Brainstorm"])
    elif category == "🗺️ Spatial":
        menu = st.sidebar.radio("Navigation", ["Property Grid Mapping", "Property Zones"])
    elif category == "📈 Analytics":
        menu = st.sidebar.radio("Navigation", ["Lake Data"])
    elif category == "⚙️ System":
        menu = st.sidebar.radio("Navigation", ["System Glossary", "Infrastructure", "Siri Setup", "Admin"])

    sim_mode = st.sidebar.toggle("Simulate AI & Data", value=True)
    st.sidebar.divider()
    st.sidebar.info(f"🌐 Server: {SERVER}")
    st.sidebar.caption(f"📁 Media Path: 02_Data/Media")

    db = SessionLocal()

    if menu == "Executive Dashboard":
        st.title("📊 Point Street Nexus Overview")
        c1, c2, c3, c4 = st.columns(4)
        
        try: c1.metric("Species", db.query(BotanicalRegistry).count())
        except: c1.metric("Species", "Error")
        try: c2.metric("Plantings", db.query(Planting).count())
        except: c2.metric("Plantings", "Error")
        try: c3.metric("Zones", db.query(PropertyZone).count())
        except: c3.metric("Zones", "Error")
        try: c4.metric("Active Tasks", db.query(Task).filter(Task.is_completed == False).count())
        except: c4.metric("Active Tasks", "Error")
        
        st.subheader("🚀 Today's Mission Tasks")
        try:
            df_tasks = pd.read_sql("SELECT name as Task, task_type as Category, priority as Priority FROM Tasks WHERE is_completed = 0 ORDER BY priority ASC", engine)
            if not df_tasks.empty: 
                st.dataframe(df_tasks, use_container_width=True, hide_index=True)
            else: st.info("No active tasks.")
        except Exception as e:
            st.error(f"Error reading Tasks table: {e}")

        st.subheader("Recent Garden Activity")
        try:
            df_recent = pd.read_sql("SELECT plant_name as Plant, status as Status, date_planted as Date FROM Plantings ORDER BY date_planted DESC", engine)
            if not df_recent.empty: 
                # Professional formatting
                st.dataframe(df_recent, use_container_width=True, hide_index=True, column_config={
                    "Date": st.column_config.DatetimeColumn("Date Planted", format="MMM DD, YYYY")
                })
            else: st.info("No recent activity.")
        except:
             st.error("Error reading Plantings table.")

    elif menu == "System Glossary":
        st.title("📖 System Glossary & Acronyms")
        st.info("Reference for all Point Street Nexus terminology.")
        try:
            df_gloss = pd.read_sql("SELECT acronym as Acronym, term as Term, definition as Definition FROM System_Glossary ORDER BY acronym ASC", engine)
            if not df_gloss.empty:
                st.dataframe(df_gloss, use_container_width=True, hide_index=True)
            else: st.info("Glossary is empty. Run seed_data.py.")
            
            with st.expander("➕ Add New Term"):
                with st.form("new_term_form"):
                    new_ac = st.text_input("Acronym (e.g., SG)")
                    new_term = st.text_input("Full Term (e.g., Sunshine Garden)")
                    new_def = st.text_area("Definition")
                    if st.form_submit_button("💾 Save Term"):
                        db.add(SystemGlossary(acronym=new_ac, term=new_term, definition=new_def))
                        db.commit()
                        st.success("Term saved!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error reading Glossary: {e}")

    elif menu == "Property Zones":
        st.title("🗺️ Property Zones & Beds")
        st.info("Manage the macro-areas of your property (Zones) and the micro-areas within them (Beds/Planters).")
        
        try:
            zones = pd.read_sql("SELECT name as Zone, description as Description FROM Property_Zones", engine)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Property Zones")
                if not zones.empty: st.dataframe(zones, use_container_width=True, hide_index=True)
                else: st.info("No zones defined.")
            
            with col2:
                st.subheader("Beds & Planters")
                query = """
                    SELECT b.name as Bed, b.bed_type as Type, z.name as Zone 
                    FROM Garden_Beds b 
                    LEFT JOIN Property_Zones z ON b.zone_id = z.zone_id
                """
                bed_zone_df = pd.read_sql(query, engine)
                if not bed_zone_df.empty:
                    st.dataframe(bed_zone_df, use_container_width=True, hide_index=True)
                else: st.info("No beds defined.")
        except Exception as e:
             st.error(f"Error reading Zone data: {e}")

    elif menu == "Species Registry":
        st.title("📖 Master Species Registry")
        try:
            df = pd.read_sql("SELECT * FROM Botanical_Registry", engine)
            if not df.empty:
                st.subheader("Species Overview")
                
                # Upgraded Data Grid with Column Config
                st.dataframe(
                    df[['species_id', 'common_name', 'plant_category', 'ai_confidence']], 
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "species_id": st.column_config.NumberColumn("ID", format="%d"),
                        "common_name": "Common Name",
                        "plant_category": "Category",
                        "ai_confidence": st.column_config.ProgressColumn(
                            "AI Confidence",
                            help="Confidence level of the AI identification",
                            format="%.2f",
                            min_value=0,
                            max_value=1,
                        )
                    }
                )
                
                st.divider()
                st.subheader("📝 Deep Dive & Edit")
                sel_s = st.selectbox("Select a Species to view Care Sheet or edit details:", options=df['common_name'].tolist())
                if sel_s:
                    row = df[df['common_name'] == sel_s].iloc[0]
                    with st.expander(f"✨ Care Sheet: {sel_s}", expanded=True):
                        new_common = st.text_input("Common Name", value=row['common_name'])
                        new_desc = st.text_area("Description", value=row['description'])
                        new_water = st.text_input("Watering", value=row['preferred_watering'])
                        new_fert = st.text_input("Fertilizer", value=row['fertilizer_needs'])
                        
                        col1, col2 = st.columns(2)
                        if col1.button("💾 Save Changes", use_container_width=True):
                            target = db.query(BotanicalRegistry).get(int(row['species_id']))
                            target.common_name = new_common
                            target.description = new_desc
                            target.preferred_watering = new_water
                            target.fertilizer_needs = new_fert
                            db.commit()
                            st.success("Changes saved!")
                            st.rerun()
                        
                        if col2.button("🗑️ Delete Species", use_container_width=True):
                            db.query(BotanicalRegistry).filter(BotanicalRegistry.species_id == int(row['species_id'])).delete()
                            db.commit()
                            st.warning(f"Deleted {sel_s}.")
                            st.rerun()

                        st.write(f"**Scientific Name:** {row['scientific_name']}")
                        st.write(f"**Sunlight:** {row['preferred_sunlight']}")
            else: st.info("Registry empty.")
        except Exception as e:
            st.error(f"Database error: {e}")

    elif menu == "Intake Center":
        st.title("📸 AI Intake & Assignment")
        t1, t2, t3 = st.tabs(["New Intake", "Batch Queue", "Assign Location"])
        with t1:
            asset_type = st.selectbox("Asset Type", ["Planting", "Property Anchor", "Project Reference", "Lidar Scan"])
            img = st.file_uploader("Upload Photo", type=["jpg","png","jpeg","heic"])
            if img and st.button("🚀 Process Intake", use_container_width=True):
                try:
                    pil_img = Image.open(img); pil_img = ImageOps.exif_transpose(pil_img)
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    if asset_type == "Planting":
                        res = identify_plant(img.getvalue(), simulate=sim_mode)
                        if res:
                            f_path = os.path.abspath(os.path.join(MEDIA_SUBDIRS["Plantings"], f"plant_{ts}.jpg"))
                            pil_img.convert("RGB").save(f_path, "JPEG")
                            
                            spec = db.query(BotanicalRegistry).filter(BotanicalRegistry.scientific_name == res["scientific_name"]).first()
                            if not spec:
                                spec = BotanicalRegistry(common_name=res["common_name"], scientific_name=res["scientific_name"], plant_category=res["plant_category"], description=res["description"], preferred_watering=res["watering"], watering_frequency_days=res["watering_days"], fertilizer_needs=res["fertilizer"], ai_confidence=res["confidence"])
                                db.add(spec); db.commit(); db.refresh(spec)
                            new_p = Planting(species_id=spec.species_id, plant_name=res["common_name"], status="Intake", date_planted=datetime.now(UTC))
                            db.add(new_p); db.commit(); db.refresh(new_p)
                            db.add(MediaAsset(file_path=f_path, entity_type="Planting", entity_id=new_p.planting_id, ai_confidence=res["confidence"], timestamp=datetime.now(UTC)))
                            db.commit(); st.balloons(); st.success(f"Saved {res['common_name']}!")
                    else:
                        if asset_type == "Property Anchor": folder = MEDIA_SUBDIRS["Property"]
                        elif asset_type == "Lidar Scan": folder = MEDIA_SUBDIRS["Lidar"]
                        else: folder = MEDIA_SUBDIRS["Projects"]
                        
                        f_path = os.path.abspath(os.path.join(folder, f"{asset_type.lower().replace(' ', '_')}_{ts}.jpg"))
                        pil_img.convert("RGB").save(f_path, "JPEG")
                        db.add(MediaAsset(file_path=f_path, entity_type=asset_type, entity_id=0, timestamp=datetime.now(UTC)))
                        db.commit(); st.success(f"Saved {asset_type} photo to {folder}!")
                except Exception as e: st.error(f"Error: {e}")
                
        with t2:
            st.subheader("📁 Batch Process Queue")
            queue_files = [f for f in os.listdir(QUEUE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.heic'))]
            st.write(f"Found **{len(queue_files)}** items in `04_Temp/intake_queue`.")
            
            if len(queue_files) > 0 and st.button(f"🚀 Batch Process {len(queue_files)} Photos", use_container_width=True):
                progress_bar = st.progress(0)
                for idx, filename in enumerate(queue_files):
                    file_path = os.path.join(QUEUE_DIR, filename)
                    try:
                        with open(file_path, "rb") as f: img_bytes = f.read()
                        pil_img = Image.open(file_path); pil_img = ImageOps.exif_transpose(pil_img)
                        res = identify_plant(img_bytes, simulate=sim_mode)
                        if res:
                            spec = db.query(BotanicalRegistry).filter(BotanicalRegistry.scientific_name == res["scientific_name"]).first()
                            if not spec:
                                spec = BotanicalRegistry(common_name=res["common_name"], scientific_name=res["scientific_name"], plant_category=res["plant_category"], description=res["description"], preferred_watering=res["watering"], fertilizer_needs=res["fertilizer"], ai_confidence=res["confidence"])
                                db.add(spec); db.commit(); db.refresh(spec)
                            new_p = Planting(species_id=spec.species_id, plant_name=res["common_name"], status="Intake", date_planted=datetime.now(UTC))
                            db.add(new_p); db.commit(); db.refresh(new_p)
                            
                            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                            final_path = os.path.abspath(os.path.join(MEDIA_SUBDIRS["Plantings"], f"plant_{ts}.jpg"))
                            pil_img.convert("RGB").save(final_path, "JPEG")
                            os.remove(file_path)
                            
                            db.add(MediaAsset(file_path=final_path, entity_type="Planting", entity_id=new_p.planting_id, ai_confidence=res["confidence"], timestamp=datetime.now(UTC)))
                            db.commit()
                    except Exception as e: st.error(f"Error processing {filename}: {e}")
                    progress_bar.progress((idx + 1) / len(queue_files))
                st.balloons(); st.success("Batch Processing Complete!"); st.rerun()

        with t3:
            try:
                unassigned = db.query(Planting).filter(Planting.bed_id == None).all()
                if unassigned:
                    p_map = {f"{p.plant_name} ({p.planting_id})": p.planting_id for p in unassigned}
                    sel_p = st.selectbox("Select Plant", options=list(p_map.keys()))
                    beds = db.query(GardenBed).all()
                    b_map = {f"{b.name}": b.bed_id for b in beds}
                    sel_b = st.selectbox("Select Target Bed", options=list(b_map.keys()))
                    if st.button("Confirm Assignment", use_container_width=True):
                        plant = db.query(Planting).get(p_map[sel_p]); plant.bed_id = b_map[sel_b]; plant.status = "In Ground"
                        db.commit(); st.success("Assigned Successfully!"); st.rerun()
                else: st.info("No unassigned plants.")
            except Exception as e:
                st.error(f"Database error: {e}")

    elif menu == "Media Asset CRUD":
        st.title("📸 Media Asset Control Center")
        try:
            df = pd.read_sql("SELECT media_id as ID, entity_type as Category, ai_confidence as Confidence, timestamp as Timestamp, file_path FROM Media_Assets ORDER BY timestamp DESC", engine)
            if not df.empty:
                asset_types = ["All"] + df['Category'].unique().tolist()
                filter_type = st.selectbox("Filter by Category", asset_types)
                if filter_type != "All": df = df[df['Category'] == filter_type]
                
                st.dataframe(
                    df[['ID', 'Category', 'Confidence', 'Timestamp']], 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "Timestamp": st.column_config.DatetimeColumn(format="MMM DD, YYYY HH:mm"),
                        "Confidence": st.column_config.ProgressColumn(format="%.2f", min_value=0, max_value=1)
                    }
                )
                sel_id = st.selectbox("Select Photo ID to View/Delete", options=df['ID'].tolist())
                row = df[df['ID'] == sel_id].iloc[0]
                if os.path.exists(row['file_path']):
                    st.image(ImageOps.exif_transpose(Image.open(row['file_path'])), use_container_width=True)
                    if st.button("🗑️ Delete Asset", use_container_width=True):
                        db.query(MediaAsset).filter(MediaAsset.media_id == int(sel_id)).delete()
                        if os.path.exists(row['file_path']): os.remove(row['file_path'])
                        db.commit(); st.rerun()
                else:
                    st.error(f"Image not found at {row['file_path']}")
            else: st.info("No media recorded.")
        except:
            st.error("Error reading Media_Assets table.")

    elif menu == "Garden Inventory":
        st.title("📂 Garden Inventory")
        try:
            df_inv = pd.read_sql("SELECT planting_id as ID, plant_name as Plant, variety as Variety, status as Status, date_planted as Planted FROM Plantings", engine)
            if not df_inv.empty: 
                # Upgraded Grid Display
                st.dataframe(
                    df_inv, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "ID": st.column_config.NumberColumn(format="%d"),
                        "Planted": st.column_config.DatetimeColumn(format="MMM DD, YYYY")
                    }
                )
            else: st.info("Inventory empty.")
        except:
            st.error("Error reading Plantings table.")

    elif menu == "Supply Inventory":
        st.title("📦 Supply & Product Inventory")
        
        with st.expander("➕ Add New Supply/Tool", expanded=False):
            with st.form("new_supply_form"):
                i_name = st.text_input("Item Name (e.g., Irish Spring Soap)")
                i_cat = st.selectbox("Category", ["Soil/Mix", "Fertilizer", "Mulch", "Pest Control", "Additive", "Container", "Tools/Equipment", "Seeds", "Propagation", "Other"])
                i_type = st.selectbox("Type", ["Organic", "Synthetic", "Homemade", "Natural", "Mixed", "N/A"])
                col1, col2 = st.columns(2)
                i_qty = col1.number_input("Quantity", min_value=0.0, value=1.0)
                i_unit = col2.selectbox("Unit", ["Bags", "Lbs", "Gallons", "Bottles", "Cubic Yards", "Items", "Bars", "Box"])
                i_loc = st.text_input("Storage Location (e.g., Garden Shed, Garage)")
                i_notes = st.text_area("Notes / Purpose")
                
                if st.form_submit_button("💾 Save to Inventory", use_container_width=True):
                    new_item = InventoryItem(
                        name=i_name, category=i_cat, type=i_type, 
                        quantity=i_qty, unit=i_unit, location=i_loc, notes=i_notes
                    )
                    db.add(new_item)
                    db.commit()
                    st.success("Item added successfully!")
                    st.rerun()

        try:
            df_supplies = pd.read_sql("SELECT item_id as ID, name as Item, category as Category, type as Type, quantity as Qty, unit as Unit, location as Location FROM Inventory_Items", engine)
            if not df_supplies.empty:
                categories = ["All"] + df_supplies['Category'].unique().tolist()
                filter_cat = st.selectbox("Filter by Category", categories)
                if filter_cat != "All":
                    df_supplies = df_supplies[df_supplies['Category'] == filter_cat]
                    
                # Upgraded Data Grid with Sorting and Formatting
                st.dataframe(
                    df_supplies, 
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "ID": st.column_config.NumberColumn(format="%d"),
                        "Qty": st.column_config.NumberColumn(format="%.1f")
                    }
                )
            else:
                st.info("No supplies recorded yet. Run the reset macro to populate initial inventory.")
        except Exception as e:
            st.error(f"Error reading Inventory_Items table. ({e})")

    elif menu == "Property Grid Mapping":
        st.title("🗺️ 10x20 Nano 300 Property Grid")
        
        if 'camera' not in st.session_state:
            st.session_state.camera = dict(eye=dict(x=1.5, y=1.5, z=1.5))

        c1, c2, c3, c4 = st.columns(4)
        if c1.button("📐 Isometric", use_container_width=True): st.session_state.camera = dict(eye=dict(x=1.25, y=1.25, z=1.25))
        if c2.button("🔝 Top View", use_container_width=True): st.session_state.camera = dict(eye=dict(x=0, y=0, z=2.0))
        if c3.button("⬅️ Side View", use_container_width=True): st.session_state.camera = dict(eye=dict(x=2.0, y=0, z=0))
        if c4.button("⬆️ Front View", use_container_width=True): st.session_state.camera = dict(eye=dict(x=0, y=2.0, z=0))

        try:
            grid_data = pd.read_sql("SELECT * FROM Property_Grid", engine)
            if not grid_data.empty:
                pivot_df = grid_data.pivot(index='grid_y', columns='grid_x', values='elevation')
                fig = go.Figure(data=[go.Surface(z=pivot_df.values, x=pivot_df.columns, y=pivot_df.index, colorscale='Viridis')])
                fig.update_layout(title='Property Topography', scene=dict(camera=st.session_state.camera), margin=dict(l=0, r=0, b=0, t=40), height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("🔥 Understanding the Heatmap & Roadmap"):
                    st.write("""
                    **Elevation Colors:**
                    - **Purple/Dark Blue**: Lowest points.
                    - **Teal/Green**: Median grade level.
                    - **Yellow/Gold**: High points.
                    
                    **Roadmap:** LiDAR Overlay, Nano 300 Sub-centimeter GPS, 360° Pano Bubbles, Google Earth Sync.
                    """)
            else:
                st.info("Property Grid data missing on R7910. Run 'seed_data.py' from XPS.")
        except:
             st.error("Error reading Property_Grid table.")

    elif menu == "Lake Data":
        st.title("🌊 Lake Norman Water Level")
        lake_level = get_lake_data(simulate=sim_mode)
        if lake_level:
            st.metric(label="Current Water Level (ft)", value=f"{lake_level:.2f}")
            st.success("🛰️ Real-time USGS Data Active.")
        else:
            sim_level = get_lake_data(simulate=True)
            st.metric(label="Current Water Level (ft)", value=f"{sim_level:.2f}")
            st.warning("⚠️ USGS Sensors Offline. Showing architect-simulated level for testing.")
        st.info("Station: MARSHALL STEAM STATION (USGS-02142501)")

    elif menu == "Projects & Brainstorm":
        st.title("📋 Project Management")
        try:
            df_t = pd.read_sql("SELECT name as Task, task_type as Type, priority as Priority, created_at as Created FROM Tasks", engine)
            if not df_t.empty: 
                st.dataframe(df_t, use_container_width=True, hide_index=True, column_config={
                    "Created": st.column_config.DatetimeColumn(format="MMM DD, YYYY")
                })
            else: st.info("No projects or tasks found.")
            
            with st.expander("💡 Brainstorm New Idea"):
                idea = st.text_input("Thought")
                if st.button("Save", use_container_width=True):
                    db.add(Task(name=idea, task_type="Brainstorm")); db.commit(); st.rerun()
        except:
             st.error("Error reading Tasks table.")

    elif menu == "Siri Setup":
        st.title("🎙️ Siri Voice Setup")
        s_url = f"http://{LOCAL_IP}:5000/brainstorm?thought="
        st.code(s_url); st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={s_url}")

    elif menu == "Infrastructure":
        st.title("🎛️ Hardware Infrastructure")
        
        tab1, tab2, tab3 = st.tabs(["Hardware", "Software", "IoT & PLCs"])
        
        with tab1:
            try:
                df_it = pd.read_sql("SELECT name as Name, type as Type, ip_address as IP, location as Location, status as Status FROM IT_Assets", engine)
                if not df_it.empty: st.dataframe(df_it, use_container_width=True, hide_index=True)
                else: st.info("No IT Assets found. Run 'seed_it_assets.py'.")
            except: st.error("Error reading IT_Assets table.")
            
        with tab2:
            try:
                df_sw = pd.read_sql("SELECT name as Name, version as Version, vendor as Vendor FROM Software_Assets", engine)
                if not df_sw.empty: st.dataframe(df_sw, use_container_width=True, hide_index=True)
                else: st.info("No Software Assets found.")
            except: st.error("Error reading Software_Assets table.")

        with tab3:
            try:
                st.subheader("IoT Hubs")
                df_hubs = pd.read_sql("SELECT name as Name, ip_address as IP FROM IoT_Hubs", engine)
                if not df_hubs.empty: st.dataframe(df_hubs, use_container_width=True, hide_index=True)
                
                st.subheader("PLC Nodes")
                df_plcs = pd.read_sql("SELECT name as Name, ip_address as IP FROM PLC_Nodes", engine)
                if not df_plcs.empty: st.dataframe(df_plcs, use_container_width=True, hide_index=True)
            except: pass

    elif menu == "Admin":
        st.title("🛠️ Admin Tools")
        if st.button("🧨 FACTORY RESET (WIPE ALL DATA)", use_container_width=True, type="primary"):
            db.close(); Base.metadata.drop_all(bind=engine); shutil.rmtree(MEDIA_DIR, ignore_errors=True); os.makedirs(MEDIA_DIR)
            init_db(); st.rerun()

    db.close()

if __name__ == "__main__":
    main()
