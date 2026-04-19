import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from database import SessionLocal, engine, init_db
from models import (Base, GardenBed, SensorReading, Planting, Task, BotanicalRegistry, 
                   IoTHub, PLCNode, PLCTag, Project, MediaAsset, PropertyGridNode)
from datetime import datetime, UTC, timedelta
import os
import requests
import base64
import traceback
import shutil
import socket
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS, GPSTAGS
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

st.set_page_config(page_title="PSN Architect V2", layout="wide", initial_sidebar_state="expanded")

# --- UI THEME ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #d1d5db; }
    h1, h2, h3 { color: #003366; }
    .stButton>button { background-color: #003366; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

MEDIA_DIR = "media"
if not os.path.exists(MEDIA_DIR): os.makedirs(MEDIA_DIR)

KEY_FILE = ".api_key"
if 'api_key' not in st.session_state:
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f: st.session_state['api_key'] = f.read().strip()
    else: st.session_state['api_key'] = ""

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
        return {
            "scientific_name": "Acer palmatum",
            "common_name": "Mock Japanese Maple",
            "description": "Simulation mode: Testing SQL and CRUD without burning API credits.",
            "plant_category": "Sapindales",
            "watering": "Medium", "watering_days": 4,
            "sunlight": "Partial Shade", "soil": "Well-drained",
            "fertilizer": "Simulated NPK 10-10-10", "growth_rate": "Moderate", "confidence": 0.99
        }
    
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
            return {
                "scientific_name": best.get("plant_name", "Unknown"),
                "common_name": det.get("common_names", ["Unknown"])[0] if det.get("common_names") else "Unknown",
                "description": det.get("description", {}).get("value", "No description."),
                "plant_category": det.get("taxonomy", {}).get("order", "Biological"),
                "watering": {1:"Low", 2:"Medium", 3:"High"}.get(w, "Medium"),
                "watering_days": det.get("watering", {}).get("min", 7),
                "sunlight": str(det.get("sunlight", {}).get("description", "Varies")),
                "soil": str(det.get("soil", {}).get("description", "Well-Drained")),
                "fertilizer": "Monthly Standard",
                "growth_rate": det.get("growth_rate", "Moderate"),
                "confidence": float(best.get("probability", 0))
            }
    except: return None
    return None

def main():
    st.sidebar.title("🌿 PSN Architect")
    
    # CREDIT SAVER TOGGLE
    st.sidebar.subheader("API Credit Control")
    simulate_mode = st.sidebar.toggle("Simulate AI Identification", value=True, help="Turn ON to test UI without using Plant.id credits.")
    
    menu = st.sidebar.radio("Navigation", 
        ["Executive Dashboard", "Species Registry", "Intake Center", "Media Asset CRUD", "Garden Inventory", "Projects & Brainstorm", "Siri Setup", "Infrastructure", "Admin"])
    
    # API Key Management
    st.sidebar.divider()
    new_key = st.sidebar.text_input("Plant.id API Key", value=st.session_state['api_key'], type="password")
    if st.sidebar.button("💾 Permanent Save Key"):
        with open(KEY_FILE, "w") as f: f.write(new_key)
        st.session_state['api_key'] = new_key; st.sidebar.success("Key Locked.")

    db = SessionLocal()

    if menu == "Intake Center":
        st.title("📸 Intake Center")
        if simulate_mode: st.warning("🛠️ SIMULATION MODE ACTIVE: No API credits will be used.")
        img = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
        if img:
            st.image(img, width=400)
            if st.button("🚀 Process Intake"):
                res = identify_plant(img.getvalue(), simulate=simulate_mode)
                if res:
                    try:
                        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                        f_path = os.path.abspath(os.path.join(MEDIA_DIR, f"intake_{ts}.jpg"))
                        with open(f_path, "wb") as f: f.write(img.getbuffer())
                        
                        spec = db.query(BotanicalRegistry).filter(BotanicalRegistry.scientific_name == res["scientific_name"]).first()
                        if not spec:
                            spec = BotanicalRegistry(common_name=res["common_name"], scientific_name=res["scientific_name"], plant_category=res["plant_category"], description=res["description"], preferred_watering=res["watering"], fertilizer_needs=res["fertilizer"], ai_confidence=res["confidence"])
                            db.add(spec); db.commit(); db.refresh(spec)
                        
                        new_p = Planting(species_id=spec.species_id, plant_name=res["common_name"], status="Intake", date_planted=datetime.now(UTC))
                        db.add(new_p); db.commit(); db.refresh(new_p)
                        
                        db.add(MediaAsset(file_path=f_path, entity_type="Planting", entity_id=new_p.planting_id, ai_confidence=res["confidence"], timestamp=datetime.now(UTC)))
                        db.commit(); st.success(f"Intake Complete (Simulated: {simulate_mode})"); st.rerun()
                    except Exception as e: st.error(f"SQL Error: {e}")

    # (Keep rest of main() logic same...)
    elif menu == "Executive Dashboard":
        st.title("📊 Point Street Nexus Overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Registry Size", db.query(BotanicalRegistry).count())
        c2.metric("Total Plantings", db.query(Planting).count())
        c3.metric("Project Tasks", db.query(Task).count())
        c4.metric("Media Assets", db.query(MediaAsset).count())

    elif menu == "Species Registry":
        st.title("📖 Master Species Registry")
        df = pd.read_sql("SELECT * FROM Botanical_Registry", engine)
        if not df.empty: AgGrid(df, key="registry_stable")

    elif menu == "Media Asset CRUD":
        st.title("📸 Media CRUD")
        df = pd.read_sql("SELECT * FROM Media_Assets", engine)
        if not df.empty:
            grid = AgGrid(df, gridOptions=GridOptionsBuilder.from_dataframe(df).configure_selection('single', use_checkbox=True).build())
            sel = grid['selected_rows']
            if sel is not None and len(sel) > 0:
                row = sel.iloc[0] if isinstance(sel, pd.DataFrame) else sel[0]
                if os.path.exists(row['file_path']): st.image(row['file_path'], width=600)

    db.close()

if __name__ == "__main__":
    main()
