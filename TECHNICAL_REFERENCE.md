# 📚 Point Street Nexus V2 - Technical Reference & Glossary

This document provides a quick reference for common commands and a glossary of terms used in the project.

---

## **🛠️ Common Commands**

### **Python (Application & Logic)**
| Command | Purpose |
| :--- | :--- |
| `python nexus_start.py` | Launches the main Streamlit dashboard AND the Siri Flask listener. |
| `python reset_db.py` | **NUCLEAR OPTION**: Wipes all data and recreates SQL tables from scratch. |
| `python cleanup_db.py` | Wipes transactional data (readings, plants) but keeps setup (Hubs, PLC). |
| `python seed_data.py` | Populates the database with sample infrastructure, tasks, and grid data. |
| `python export_plant_data.py` | Saves current plant and media metadata to CSV files in the `backups/` folder. |
| `python import_plant_data.py` | Restores plant and media data from CSV files in the `backups/` folder. |
| `python -m pip install <package>` | Installs a new Python library (e.g., `pillow-heif`, `sqlalchemy`). |

### **PowerShell (Terminal & File Management)**
| Command | Purpose |
| :--- | :--- |
| `ls` or `dir` | Lists all files and folders in the current directory. |
| `cd <folder_name>` | Changes the current directory to the specified folder. |
| `cd ..` | Moves up one level in the directory structure. |
| `ping <IP_ADDRESS>` | Tests the network connection to another device (e.g., `ping 192.168.1.245`). |
| `clear` or `cls` | Clears the terminal screen. |

### **Git (Version Control)**
| Command | Purpose |
| :--- | :--- |
| `git add .` | Stages all changed files for the next "save point" (commit). |
| `git commit -m "Message"` | Saves a new version of your code with a descriptive message. |
| `git push origin main` | Uploads your saved versions to the master repository on GitHub. |
| `git pull origin main` | Downloads the latest version of the code from GitHub to your machine. |
| `git status` | Shows which files have been changed and what is staged for commit. |
| `git log -n 5` | Shows a history of the last 5 versions (commits). |

### **SQL (Database Management - Run in SSMS)**
| Query | Purpose |
| :--- | :--- |
| `SELECT * FROM <TableName>` | Displays all data from a specific table. |
| `DELETE FROM <TableName>` | Deletes all records from a table (Warning: permanent!). |
| `EXEC sys.sp_readerrorlog 0, 1, 'listening'` | Finds the port number the SQL Server is currently using. |

---

## **📖 Glossary of Terms**

| Term | Definition |
| :--- | :--- |
| **XPS** | Your Dell XPS laptop, used as the **Master Development** machine. |
| **R7910** | Your Dell Precision R7910 server (**TheSharkEngine**), used for **Production**. |
| **SQL Server** | The database engine (Microsoft SQL Server) that stores all project data. |
| **Streamlit** | The Python framework used to build the web-based "Architect Dashboard." |
| **Flask** | The Python framework used to build the "Siri Setup" listener. |
| **Ag-Grid** | A high-performance interactive data grid used for tables in the dashboard. |
| **HEIC** | High Efficiency Image Format - the default photo format for newer iPhones. |
| **plant.id** | The AI service used to identify plants from photos. |
| **L32E** | Your Allen-Bradley CompactLogix PLC, used for garden automation. |
| **Hubitat** | Your home automation hub, used for moisture sensors and smart devices. |
| **Nano 300** | A high-precision LiDAR/scanning system for creating topographic maps. |
| **Commit** | A "save point" in Git that captures the current state of your code. |
| **Push / Pull** | The process of uploading code to (Push) or downloading code from (Pull) GitHub. |
| **Schema** | The structure or "blueprint" of your database tables and columns. |
| **CRUD** | **C**reate, **R**ead, **U**pdate, **D**elete - the four basic functions of persistent storage. |
