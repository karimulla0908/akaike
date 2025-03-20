import subprocess
import time
import os
import threading

def start_api_server():
    print("Starting FastAPI server...")
    api_process = subprocess.Popen(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"], 
                                  stdout=subprocess.PIPE)
    
    # Wait for server to start
    for line in iter(api_process.stdout.readline, b''):
        line_text = line.decode('utf-8').strip()
        print(f"API: {line_text}")
        if "Application startup complete" in line_text:
            print("API server is ready!")
            break
    
    return api_process

def start_streamlit():
    print("Starting Streamlit app...")
    streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"],
                                        stdout=subprocess.PIPE)
    
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
