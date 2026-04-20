import subprocess
import time
import sys
import os

def start_nexus():
    print("🚀 Starting Point Street Nexus V2 Services...")

    # 1. Start the Siri Brainstorm Listener (Flask)
    print("📡 Launching Siri Listener on Port 5000...")
    # Use sys.executable to ensure we use the virtual environment's python
    siri_proc = subprocess.Popen([sys.executable, "siri_brainstorm.py"])

    # 2. Start the Streamlit Dashboard
    print("🌿 Launching Streamlit Dashboard on Port 8501...")
    # Using 'python -m streamlit run app.py' is more robust on Windows than calling 'streamlit' directly
    streamlit_proc = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])

    print("\n✅ All systems active.")
    print(f"--- Dashboard: http://localhost:8501")
    print(f"--- Siri API:  http://{socket.gethostbyname(socket.gethostname()) if 'socket' in sys.modules else 'localhost'}:5000")
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
    # Import socket here for the IP printout
    import socket
    start_nexus()
