import subprocess
import time
import os
import threading
import socket
import psutil

def is_port_in_use(port: int) -> bool:
    """Checks if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def terminate_process_on_port(port: int):
    """Terminates processes listening on the given port."""
    for proc in psutil.process_iter(['pid', 'connections', 'addr']): #add addr to process_iter
        try:
            if 'connections' in proc.info and proc.info['connections']: #check if connections attribute exists
                connections = proc.info['connections']
                for conn in connections:
                    if conn.laddr.port == port:
                        print(f"Terminating process {proc.info['pid']} using port {port}")
                        process = psutil.Process(proc.info['pid'])
                        process.terminate()
                        process.wait()  # Wait for process termination
                        return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, KeyError): #add KeyError
            pass  # Ignore exceptions if process no longer exists or attribute is missing

    return False


def start_api_server(port=8000):
    """Starts FastAPI server after checking and terminating existing process on port."""
    if is_port_in_use(port):
        print(f"Port {port} is already in use.")
        if terminate_process_on_port(port):
            time.sleep(1)  # Give time to terminate
            if is_port_in_use(port):
                print(f"Failed to terminate process on port {port}. Exiting.")
                return None
        else:
            print(f"No process found to terminate on port {port}. Exiting.")
            return None

    print(f"Starting FastAPI server on port {port}...")
    api_process = subprocess.Popen(
        ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
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
    """Starts Streamlit app in the main thread."""
    print("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "app.py"])

# Main script
if __name__ == "__main__":
    # Start API server and wait for it to be ready
    api_process = start_api_server()

    if api_process is None:
        exit(1)  # Exit if API server did not start

    # Start Streamlit in the main thread
    start_streamlit()

    try:
        # Keep the main process running (needed for API server)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        api_process.terminate()
