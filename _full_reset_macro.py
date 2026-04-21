import subprocess
import sys

def run_script(script_name):
    print(f"\n[{script_name}] >> Starting...")
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"[{script_name}] >> SUCCESS")
    except subprocess.CalledProcessError:
        print(f"[{script_name}] >> FAILED. Stopping Macro.")
        sys.exit(1)

if __name__ == "__main__":
    print("=======================================")
    print("   ARCHITECT FULL RESET MACRO   ")
    print("=======================================")
    
    # 1. Save data
    run_script("export_plant_data.py")
    
    # 2. Rebuild Database Schema
    run_script("reset_db.py")
    
    # 3. Restore Data
    run_script("import_plant_data.py")
    
    # 4. Seed Infrastructure
    run_script("seed_data.py")
    run_script("seed_it_assets.py")
    run_script("init_mission_tasks.py")
    
    print("\n=======================================")
    print("   MACRO COMPLETE! System Ready.   ")
    print("=======================================")
