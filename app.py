import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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

def main():
    st.sidebar.title("🌿 PSN Architect")
    sim_mode = st.sidebar.toggle("Simulate AI & Data", value=True)
    menu = st.sidebar.radio("Navigation", 
        ["Executive Dashboard", "Species Registry", "Intake Center", "Media Asset CRUD", "Garden Inventory", "Property Grid Mapping", "Lake Data", "Projects & Brainstorm", "Siri Setup", "Infrastructure", "Admin"])
    
    st.sidebar.divider()
    st.sidebar.info(f"🌐 Server: {SERVER}")

    db = SessionLocal()

    if menu == "Lake Data":
        st.title("🌊 Lake Norman Water Level")
        
        # TRY REAL DATA FIRST
        lake_level = get_lake_data(simulate=False)
        
        if lake_level:
            st.metric(label="Current Water Level (ft)", value=f"{lake_level:.2f}")
            st.success("🛰️ Real-time USGS Data Active.")
        else:
            # AUTO-FAILOVER TO SIMULATION
            sim_level = get_lake_data(simulate=True)
            st.metric(label="Current Water Level (ft)", value=f"{sim_level:.2f}")
            st.warning("⚠️ USGS Sensors Offline. Showing architect-simulated level for testing.")
            
        st.info("Station: CATAWBA RIVER AT MARSHALL STEAM STATION (USGS-02142501)")

    # (Other pages remain same...)
    elif menu == "Executive Dashboard":
        st.title("📊 Point Street Nexus Overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Species", db.query(BotanicalRegistry).count())
        c2.metric("Plantings", db.query(Planting).count())
        c3.metric("Photos", db.query(MediaAsset).count())
        c4.metric("Tasks", db.query(Task).count())

    db.close()

if __name__ == "__main__":
    main()
