import subprocess
import time
import os
import threading
import socket

def is_port_in_use(port: int) -> bool:
    """Checks if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_api_server(port=8000):
    """Starts FastAPI server, trying different ports if necessary."""
    while is_port_in_use(port):
        print(f"Port {port} is already in use. Trying port {port + 1}...")
        port += 1

    print(f"Starting FastAPI server on port {port}...")
    api_process = subprocess.Popen(
        ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, #to capture error logs in the same pipe
    )

    # Wait for server to start
    for line in iter(api_process.stdout.readline, b''):
        line_text = line.decode('utf-8').strip()
        print(f"API: {line_text}")
        if "Application startup complete" in line_text:
            print(f"API server is ready on port {port}!")
            break

    return api_process

def start_streamlit():
    print("Starting Streamlit app...")
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, #added stderr to capture errors in same pipe
    )

    # Print Streamlit output
    for line in iter(streamlit_process.stdout.readline, b''):
        print(f"Streamlit: {line.decode('utf-8').strip()}")

# Main script
if __name__ == "__main__":
    # Start API server and wait for it to be ready
    api_process = start_api_server()

    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=start_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()

    try:
        # Keep the main process running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        api_process.terminate()
