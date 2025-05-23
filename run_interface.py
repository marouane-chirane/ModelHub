import subprocess
import sys
import os

def run_streamlit():
    """Lance l'interface Streamlit."""
    streamlit_path = os.path.join("app", "interface", "streamlit_app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_path])

if __name__ == "__main__":
    run_streamlit() 