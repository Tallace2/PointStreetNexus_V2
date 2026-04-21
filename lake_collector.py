import requests
import random

# We will try a few different station candidates for Lake Norman area
# 02142501 is Catawba River NR Eleazer, NC (upstream / Lake Norman)
STATIONS = ["02142501", "02142500", "02142502", "02142503"]
PARAMS = ["00062", "00065"] # Reservoir elevation (00062) or Gage height (00065)

def get_lake_data(simulate=False):
    if simulate:
        # Return a plausible simulated lake level
        simulated_level = round(random.uniform(97.5, 98.5), 2)
        print(f"DEBUG: SIMULATION MODE ACTIVE - Returning simulated lake level: {simulated_level} ft")
        return simulated_level

    for station in STATIONS:
        for param in PARAMS:
            url = f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={station}&parameterCd={param}&siteStatus=all"
            try:
                print(f"DEBUG: Trying Station {station}, Param {param}...")
                response = requests.get(url, timeout=5)
                if response.status_code != 200:
                    continue
                    
                data = response.json()
                time_series = data.get('value', {}).get('timeSeries', [])
                
                if time_series and time_series[0].get('values'):
                    values = time_series[0]['values'][0].get('value', [])
                    if values:
                        latest_value = values[-1]['value']
                        site_name = time_series[0]['sourceInfo']['siteName']
                        
                        print(f"DEBUG: SUCCESS! Found data at {site_name}: {latest_value} ft")
                        return float(latest_value)
            except Exception as e:
                print(f"DEBUG: Error for Station {station}, Param {param}: {e}")
                continue
                
    print("DEBUG: Exhausted all USGS station/parameter combinations. No active data found.")
    return None

if __name__ == "__main__":
    print("--- Testing Real Data Fetch ---")
    val_real = get_lake_data(simulate=False)
    print(f"Real Result: {val_real}")
    
    print("\n--- Testing Simulation Data Fetch ---")
    val_sim = get_lake_data(simulate=True)
    print(f"Simulated Result: {val_sim}")
