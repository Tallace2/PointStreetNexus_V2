import os

def init_folders():
    folders = [
        "02_Data",
        "02_Data/Media",
        "02_Data/Media/plantings",
        "02_Data/Media/property_anchors",
        "02_Data/Media/lidar_scans",
        "02_Data/Media/projects",
        "03_Automation",
        "04_Temp",
        "04_Temp/intake_queue"
    ]
    
    print("Initializing Architect Folder Structure...")
    for folder in folders:
        # Use absolute path based on current directory
        path = os.path.abspath(folder)
        os.makedirs(path, exist_ok=True)
        print(f"Verified: {path}")

if __name__ == "__main__":
    init_folders()
