import requests
from database import SessionLocal
from models import IoTHub, IoTDevice, SensorNode, SensorReading, Task
from datetime import datetime

def sync_hubitat_data():
    db = SessionLocal()
    try:
        hubs = db.query(IoTHub).all()
        
        for hub in hubs:
            if not hub.ip_address or not hub.api_key:
                print(f"Skipping {hub.name} - No IP or API Key found.")
                continue

            print(f"\n--- Syncing Hub: {hub.name} ({hub.ip_address}) ---")
            
            # Using the 'model' field where we stored the App ID
            app_id = hub.model if hub.model else "171" 
            access_token = hub.api_key
            
            devices = db.query(IoTDevice).filter(IoTDevice.hub_id == hub.hub_id).all()
            
            if not devices:
                print(f"No devices found for {hub.name} in SQL. Run discovery script?")
                continue

            for device in devices:
                print(f"Polling Device: {device.name} (ID: {device.device_id})")
                
                try:
                    url = f"http://{hub.ip_address}/apps/api/{app_id}/devices/{device.device_id}?access_token={access_token}"
                    resp = requests.get(url, timeout=5)
                    data = resp.json()

                    attributes = data.get("attributes", [])
                    moisture = next((a["currentValue"] for a in attributes if a["name"] == "humidity"), None)
                    temp = next((a["currentValue"] for a in attributes if a["name"] == "temperature"), None)

                    if moisture is not None:
                        s_node = db.query(SensorNode).filter(SensorNode.iot_device_id == device.device_id).first()
                        if s_node:
                            new_reading = SensorReading(
                                sensor_id=s_node.sensor_id,
                                soil_moisture=float(moisture),
                                temperature=float(temp) if temp else None,
                                timestamp=datetime.utcnow()
                            )
                            db.add(new_reading)
                            print(f"   [SUCCESS] Recorded: Moisture {moisture}% | Temp {temp}F")
                except Exception as e:
                    print(f"   [ERROR] Failed to poll device {device.device_id}: {e}")

        # Auto-update task list status
        hub_task = db.query(Task).filter(Task.name.like("%Hubitat%")).first()
        if hub_task:
            hub_task.is_completed = True
            
        db.commit()
        print("\nHubitat Sync Complete.")

    except Exception as e:
        print(f"Error during sync: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    sync_hubitat_data()
