from pylogix import PLC
from database import SessionLocal
from models import PLCNode, PLCTag, SensorReading, Task
from datetime import datetime

def check_and_water():
    db = SessionLocal()
    try:
        # 1. Get the L32E Configuration from SQL
        plc_info = db.query(PLCNode).filter(PLCNode.name.like("%Irrigation%")).first()
        if not plc_info:
            print("PLC Node not found in database.")
            return

        print(f"--- Connecting to CompactLogix L32E: {plc_info.ip_address} (Slot 0) ---")
        
        # 2. Initialize the Pylogix driver
        with PLC() as comm:
            comm.IPAddress = plc_info.ip_address
            comm.ProcessorSlot = 0  # CompactLogix CPU is always Slot 0
            
            # 3. Process each Solenoid Tag
            tags = db.query(PLCTag).filter(PLCTag.plc_id == plc_info.plc_id).all()
            
            for tag in tags:
                # Get latest moisture for this bed (e.g., RB1)
                bed_prefix = tag.tag_name.split('_')[0] 
                sensor_id = f"SSMS-G2-{bed_prefix}"
                
                reading = db.query(SensorReading).filter(
                    SensorReading.sensor_id == sensor_id
                ).order_by(SensorReading.timestamp.desc()).first()

                if reading:
                    moisture = reading.soil_moisture
                    # Logic: Threshold check
                    is_dry = moisture < 25.0 
                    
                    print(f"Bed {bed_prefix}: {moisture}% moisture. Command -> {'ON' if is_dry else 'OFF'}")
                    
                    # 4. Write to the L32E Tag
                    # The tag name must exist in the L32E Controller Tags
                    ret = comm.Write(tag.tag_name, is_dry)
                    
                    if ret.Status == "Success":
                        print(f"   [OK] Tag {tag.tag_name} updated successfully.")
                    else:
                        print(f"   [ERROR] Could not write to {tag.tag_name}: {ret.Status}")
                else:
                    print(f"   [SKIP] No sensor data for {sensor_id}")

        # Update Task Status
        plc_task = db.query(Task).filter(Task.name.like("%PLC%")).first()
        if plc_task:
            plc_task.is_completed = True
            db.commit()

    except Exception as e:
        print(f"PLC Communication Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_and_water()
