# 🌿 Point Street Nexus V3.1 - System Blueprint

## 🏗️ Architecture Overview
- **Master Development (XPS)**: PyCharm coding, UI design, and logic testing.
- **Production Server (TheSharkEngine - R7910)**: `192.168.1.245`. Hosts the SQL Server and the Production Streamlit App.
- **Client (iPhone 17 Pro Max)**: Accesses the Web UI via `http://192.168.1.245:8501` (when in production) or `http://192.168.1.18:8501` (when testing on XPS).

## 💾 Database Configuration (SQL Server)
- **Host**: `192.168.1.245,55658` (TheSharkEngine)
- **Auth**: SQL Server Authentication (`sa`)
- **Schema Features**: 
  - **Horticulture**: Botanical Registry, Plantings, Garden Beds, Property Zones.
  - **Operations**: Supply Inventory (Fertilizers, Tools, Mulch), Project Management, Tasks.
  - **Spatial**: 10x20 Nano 300 Property Grid (3D Topography).
  - **System**: System Glossary, IT Assets, Software Assets, IoT Hubs, PLC Nodes.

## 📁 File System & Media Storage
- **Primary Drive**: The system is hard-coded to prioritize the `S:/01_Development/PointStreetNexus_V2` drive for high-volume media storage.
- **Failover**: If the `S:` drive is unmapped, it defaults to the local `C:` drive project folder.
- **Folder Structure**:
  - `02_Data/Media/plantings`: AI-processed plant photos.
  - `02_Data/Media/property_anchors`: Structural reference photos.
  - `04_Temp/intake_queue`: The drop-zone for batch processing field photos.

## 🚀 Key Features
1. **AI Batch Intake**: Drop field photos into the `intake_queue` to automatically process them through Plant.id and sync to SQL.
2. **3D Property Grid**: Interactive topography map with Isometric, Top, Side, and Front views.
3. **Infrastructure Management (IMS)**: Track servers, laptops, PLCs, and software licenses.
4. **Lake Data**: Real-time integration with USGS API (Marshall Steam Station) with simulation failover.
5. **Siri Voice**: Flask Listener (Port 5000) for dictating Brainstorm ideas directly to SQL.

## 🛠️ Maintenance Commands
- **Launch System**: `python nexus_start.py`
- **Nuclear Reset Macro**: `python _full_reset_macro.py` (Exports data, wipes DB, rebuilds schema, imports data, seeds infrastructure).
- **Code Sync to R7910**: 
  - On XPS: `git add .`, `git commit -m "..."`, `git push origin main`
  - On R7910: `git pull origin main`, `python nexus_start.py`
