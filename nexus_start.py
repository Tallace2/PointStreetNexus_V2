import subprocess
import time
import sys

def start_nexus():
    print("🚀 Starting Point Street Nexus V2 Services...")

    # 1. Start the Siri Brainstorm Listener (Flask)
    print("📡 Launching Siri Listener on Port 5000...")
    siri_proc = subprocess.Popen([sys.executable, "siri_brainstorm.py"])

    # 2. Start the Streamlit Dashboard
    print("🌿 Launching Streamlit Dashboard on Port 8501...")
    # Using 'streamlit run' directly via subprocess
    streamlit_proc = subprocess.Popen(["streamlit", "run", "app.py"])

    print("\n✅ All systems active.")
    print("--- Dashboard: http://localhost:8501")
    print("--- Siri API:  http://localhost:5000")
    print("\nPress Ctrl+C in this terminal to shut down all services.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Nexus services...")
        siri_proc.terminate()
        streamlit_proc.terminate()
        print("Done.")

if __name__ == "__main__":
    start_nexus()
