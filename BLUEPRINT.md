# 🌿 Point Street Nexus V2 - System Blueprint

## 🏗️ Architecture Overview
- **Master Development (XPS)**: PyCharm coding and logic testing.
- **Production Server (TheSharkEngine - R7910)**: 192.168.1.245.
- **Client (iPhone 17 Pro Max)**: Accesses the XPS Web UI via `http://192.168.1.18:8501`.

## 💾 Database Configuration (SQL Server)
- **Host**: 192.168.1.245 (R7910)
- **Port**: 55658 (SQLEXPRESS Dynamic Port)
- **Auth**: SQL Server Authentication (`sa`)
- **Schema**: Rich Botanical Data (Fertilizer, Category, AI Confidence, Variety, Health Score).

## 🚀 Key Features
1. **AI Intake**: iPhone HEIC Support -> Automatic JPG Conversion -> Remote SQL Sync.
2. **Mobile CRUD**: Vertical "Care Sheets" optimized for iPhone screens with Edit/Save/Delete.
3. **Siri Voice**: Flask Listener (Port 5000) for dictating Brainstorm ideas directly to SQL.
4. **Hardware**: Dual Hubitat Integration + Allen-Bradley L32E PLC Tag Mapping.
5. **Terrain**: 10x20 Property Grid with 3D Plotly Elevation Visualization.

## 🛠️ Maintenance Commands
- **Launch System**: `python nexus_start.py`
- **Full Wipe**: `python reset_db.py`
- **Soft Cleanup**: `python cleanup_db.py`
- **Populate Samples**: `python seed_data.py`
