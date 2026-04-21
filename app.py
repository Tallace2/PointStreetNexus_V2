import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from database import SessionLocal, engine, init_db, SERVER
from models import (Base, GardenBed, SensorReading, Planting, Task, BotanicalRegistry, 
                   IoTHub, PLCNode, PLCTag, Project, MediaAsset, PropertyGridNode)
from datetime import datetime, UTC, timedelta
import os
import requests
import base64
import shutil
import socket
from PIL import Image, ImageOps

# Support for HEIC
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

# Import the lake data collector
from lake_collector import get_lake_data

# --- PAGE CONFIG ---
st.set_page_config(page_title="PSN Architect V2", layout="wide", initial_sidebar_state="expanded")

# --- UI THEME ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #d1d5db; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #003366; color: white; border-radius: 8px; height: 3em; }
    /* Mobile Table Fix */
    .stDataFrame { overflow-x: auto; }
    </style>
    """, unsafe_allow_html=True)

MEDIA_DIR = "media"
if not os.path.exists(MEDIA_DIR): os.makedirs(MEDIA_DIR)

KEY_FILE = ".api_key"
if 'api_key' not in st.session_state:
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f: st.session_state['api_key'] = f.read().strip()
    else:
        st.session_state['api_key'] = ""

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1)); IP = s.getsockname()[0]
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
    st.sidebar.title("🌿 PSN Architect")
    sim_mode = st.sidebar.toggle("Simulate AI & Data", value=True)
    menu = st.sidebar.radio("Navigation", 
        ["Executive Dashboard", "Species Registry", "Intake Center", "Media Asset CRUD", "Garden Inventory", "Property Grid Mapping", "Lake Data", "Projects & Brainstorm", "Siri Setup", "Infrastructure", "Admin"])
    
    st.sidebar.divider()
    st.sidebar.info(f"🌐 Server: {SERVER}")

    db = SessionLocal()

    if menu == "Property Grid Mapping":
        st.title("🗺️ 10x20 Nano 300 Property Grid")
        
        # Camera State Management
        if 'camera' not in st.session_state:
            st.session_state.camera = dict(eye=dict(x=1.5, y=1.5, z=1.5))

        # View Buttons
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("📐 Isometric"): st.session_state.camera = dict(eye=dict(x=1.25, y=1.25, z=1.25))
        if c2.button("🔝 Top View"): st.session_state.camera = dict(eye=dict(x=0, y=0, z=2.0))
        if c3.button("⬅️ Side View"): st.session_state.camera = dict(eye=dict(x=2.0, y=0, z=0))
        if c4.button("⬆️ Front View"): st.session_state.camera = dict(eye=dict(x=0, y=2.0, z=0))

        grid_data = pd.read_sql("SELECT * FROM Property_Grid", engine)
        if not grid_data.empty:
            pivot_df = grid_data.pivot(index='grid_y', columns='grid_x', values='elevation')
            z_data = pivot_df.values
            
            fig = go.Figure(data=[go.Surface(
                z=z_data, 
                x=pivot_df.columns, 
                y=pivot_df.index,
                colorscale='Viridis', # Professional terrain scale
                colorbar=dict(title='Elevation (ft)')
            )])
            
            fig.update_layout(
                title='Property Topography (Current Scan)',
                scene=dict(
                    xaxis_title='X (ft)',
                    yaxis_title='Y (ft)',
                    zaxis_title='Elevation (ft)',
                    camera=st.session_state.camera
                ),
                margin=dict(l=0, r=0, b=0, t=40),
                height=700
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # --- ARCHITECT'S LEGEND & ROADMAP ---
            st.divider()
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader("🔥 Understanding the Heatmap")
                st.write("""
                The colors represent **Elevation (Z-Axis)**:
                - **Purple/Dark Blue**: Lowest points of the property.
                - **Teal/Green**: Median grade level.
                - **Yellow/Gold**: High points (ideal for solar or vantage points).
                """)
            
            with col_right:
                st.subheader("🛰️ Mapping Roadmap")
                st.info("""
                **Currently Displaying**: 10x20 Coarse Topography (Sample Nodes).
                
                **Coming Soon**:
                1. **LiDAR Overlay**: Millions of points for precise tree-line and structure detection.
                2. **Nano 300 Integration**: Sub-centimeter GPS accuracy for node placement.
                3. **360° Pano Bubbles**: Click a grid node to see a high-res iPhone panorama from that spot.
                4. **Google Earth Sync**: Drape this 3D mesh over actual satellite imagery.
                """)
        else:
            st.info("Property Grid is currently empty.")

    # (Other pages remain same...)
    elif menu == "Executive Dashboard":
        st.title("📊 Overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Species", db.query(BotanicalRegistry).count())
        c2.metric("Plantings", db.query(Planting).count())
        c3.metric("Photos", db.query(MediaAsset).count())
        c4.metric("Tasks", db.query(Task).count())
        
        st.subheader("🚀 Today's Mission Tasks")
        df_tasks = pd.read_sql("SELECT name, task_type, priority FROM Tasks WHERE is_completed = 0 ORDER BY priority ASC", engine)
        if not df_tasks.empty: st.table(df_tasks)

    elif menu == "Species Registry":
        st.title("📖 Master Species Registry")
        df = pd.read_sql("SELECT * FROM Botanical_Registry", engine)
        if not df.empty:
            st.dataframe(df[['species_id', 'common_name', 'plant_category', 'ai_confidence']], use_container_width=True)
            sel_s = st.selectbox("🔍 View Detail", options=df['common_name'].tolist())
            row = df[df['common_name'] == sel_s].iloc[0]
            with st.expander(f"Care Sheet: {sel_s}", expanded=True):
                st.write(f"**Scientific Name:** {row['scientific_name']}")
                st.write(f"**Fertilizer:** {row['fertilizer_needs']}")
                st.info(row['description'])

    elif menu == "Intake Center":
        st.title("📸 AI Intake")
        img = st.file_uploader("Upload Plant Photo", type=["jpg","png","jpeg","heic"])
        if img and st.button("🚀 Process Full Intake"):
            try:
                pil_img = Image.open(img); pil_img = ImageOps.exif_transpose(pil_img)
                res = identify_plant(img.getvalue(), simulate=sim_mode)
                if res:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    f_path = os.path.abspath(os.path.join(MEDIA_DIR, f"intake_{ts}.jpg"))
                    pil_img.convert("RGB").save(f_path, "JPEG")
                    spec = db.query(BotanicalRegistry).filter(BotanicalRegistry.scientific_name == res["scientific_name"]).first()
                    if not spec:
                        spec = BotanicalRegistry(common_name=res["common_name"], scientific_name=res["scientific_name"], plant_category=res["plant_category"], description=res["description"], preferred_watering=res["watering"], watering_frequency_days=res["watering_days"], fertilizer_needs=res["fertilizer"], ai_confidence=res["confidence"])
                        db.add(spec); db.commit(); db.refresh(spec)
                    new_p = Planting(species_id=spec.species_id, plant_name=res["common_name"], status="Intake", date_planted=datetime.now(UTC))
                    db.add(new_p); db.commit(); db.refresh(new_p)
                    db.add(MediaAsset(file_path=f_path, entity_type="Planting", entity_id=new_p.planting_id, ai_confidence=res["confidence"], timestamp=datetime.now(UTC)))
                    db.commit(); st.balloons(); st.success(f"Saved {res['common_name']}!")
            except Exception as e: st.error(f"Error: {e}")

    elif menu == "Media Asset CRUD":
        st.title("📸 Media Assets")
        df = pd.read_sql("SELECT * FROM Media_Assets", engine)
        if not df.empty:
            st.dataframe(df[['media_id', 'entity_id', 'ai_confidence', 'timestamp']], use_container_width=True)
            sel_id = st.selectbox("View ID", options=df['media_id'].tolist())
            row = df[df['media_id'] == sel_id].iloc[0]
            if os.path.exists(row['file_path']): st.image(row['file_path'], width=600)
        else: st.info("No media.")

    elif menu == "Lake Data":
        st.title("🌊 Lake Level")
        lake_level = get_lake_data(simulate=sim_mode)
        st.metric(label="Current Level (ft)", value=f"{lake_level:.2f}")
        st.info("Station: MARSHALL STEAM STATION (USGS-02142501)")

    elif menu == "Garden Inventory":
        st.title("📂 Inventory")
        df = pd.read_sql("SELECT * FROM Plantings", engine)
        if not df.empty: st.dataframe(df, use_container_width=True)

    elif menu == "Projects & Brainstorm":
        st.title("📋 Projects")
        df_t = pd.read_sql("SELECT * FROM Tasks", engine)
        if not df_t.empty: st.dataframe(df_t, use_container_width=True)
        with st.expander("💡 Brainstorm New Idea"):
            idea = st.text_input("Thought")
            if st.button("Save"):
                db.add(Task(name=idea, task_type="Brainstorm")); db.commit(); st.rerun()

    elif menu == "Siri Setup":
        st.title("🎙️ Siri Setup")
        s_url = f"http://{LOCAL_IP}:5000/brainstorm?thought="
        st.code(s_url); st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={s_url}")

    elif menu == "Infrastructure":
        st.title("🎛️ Infrastructure")
        st.subheader("IoT Hubs")
        st.table(pd.read_sql("SELECT * FROM IoT_Hubs", engine))
        st.subheader("PLC Nodes")
        st.table(pd.read_sql("SELECT * FROM PLC_Nodes", engine))

    elif menu == "Admin":
        st.title("🛠️ Admin")
        if st.button("🧨 WIPE ALL TABLES"):
            db.close(); Base.metadata.drop_all(bind=engine); shutil.rmtree(MEDIA_DIR, ignore_errors=True); os.makedirs(MEDIA_DIR)
            init_db(); st.rerun()

    db.close()

if __name__ == "__main__":
    main()
