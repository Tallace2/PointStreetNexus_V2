# 📚 Point Street Nexus V2 - Learning Reference

## 🚀 Daily Workflow
1. **Start System**: `python nexus_start.py`
2. **Backup Data**: `python export_plant_data.py`
3. **Wipe/Update Schema**: `python reset_db.py`
4. **Restore Data**: `python import_plant_data.py`
5. **Lock Version**: `git add .` -> `git commit -m "Labels"`

## 🛠️ The "Big Three" Terminal Languages

### 1. Python (The Logic)
Python runs your scripts. 
- Use `python <filename>.py` to run.
- Use `pip` to install new capabilities.

### 2. PowerShell (The Environment)
Windows command line.
- `ls` or `dir`: See files in folder.
- `ping`: Check network heartbeat.
- `cd`: Change directory.

### 3. SQL (The Memory)
The language of the database.
- `SELECT`: "Show me..."
- `UPDATE`: "Change this..."
- `DROP`: "Destroy table..."

## 🗺️ Mapping Definitions
- **Z-Axis**: Elevation (Height).
- **ISO View**: 3D perspective looking down at an angle.
- **Top View**: Bird's eye "Blueprint" view.
- **Heatmap**: Color-coding data (e.g., higher ground is yellow).

## 📡 Networking
- **SharkEngine IP**: 192.168.1.245
- **SQL Port**: 55658
- **UI Port**: 8501
- **Siri Port**: 5000
