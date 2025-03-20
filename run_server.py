import subprocess
import time
import os
import sys
import threading

def run_fastapi():
    """Run the FastAPI server"""
    print("Starting FastAPI server...")
    subprocess.run(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"])

def run_streamlit():
    """Run the Streamlit app"""
    print("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "app.py"])

def main():
    # Start FastAPI in a separate thread
    api_thread = threading.Thread(target=run_fastapi)
    api_thread.daemon = True
    api_thread.start()
    
    # Wait for FastAPI to start
    print("Waiting for FastAPI server to start...")
    time.sleep(5)
    
    # Start Streamlit in the main thread
    run_streamlit()

if __name__ == "__main__":
    main()
