import subprocess
import time
import os
import sys
import threading
import socket
import requests

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def wait_for_api_server(timeout=30):
    """Wait for the API server to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://0.0.0.0:8000/docs")
            if response.status_code == 200:
                print("FastAPI server is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
        print("Waiting for FastAPI server to start...")
    
    print("Timed out waiting for FastAPI server")
    return False

def run_fastapi(port=8000):
    """Run the FastAPI server"""
    if is_port_in_use(port):
        print(f"Port {port} is already in use. Assuming FastAPI is already running.")
        return
    
    print(f"Starting FastAPI server on port {port}...")
    subprocess.Popen(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", str(port)])

def run_streamlit():
    """Run the Streamlit app"""
    print("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "app.py"])

def main():
    # Start FastAPI
    port = 8000
    run_fastapi(port)
    
    # Wait for FastAPI to start or detect if it's already running
    if not is_port_in_use(port):
        wait_for_api_server()
    else:
        print("FastAPI appears to be already running.")
    
    # Start Streamlit in the main thread
    run_streamlit()

if __name__ == "__main__":
    main()
