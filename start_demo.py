import os
import sys
import webbrowser
import subprocess
import time
import signal
import platform
import requests
from pathlib import Path

def start_server():
    """Start the FastAPI server"""
    print("Starting the server...")
    
    # Determine the Python executable to use
    python_cmd = sys.executable
    
    # Start the server as a subprocess
    server_process = subprocess.Popen(
        [python_cmd, "src/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for the server to start
    print("Waiting for server to start...")
    
    # Wait for the server to be ready
    max_attempts = 10
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get("http://localhost:8000/docs")
            if response.status_code == 200:
                print("Server is ready!")
                break
        except requests.exceptions.ConnectionError:
            pass
        
        attempts += 1
        time.sleep(2)
    
    if attempts == max_attempts:
        print("Warning: Could not confirm server is running. Proceeding anyway...")
    
    return server_process

def open_demo():
    """Open the demo interface in a web browser"""
    # Use the server URL instead of file path
    demo_url = "http://localhost:8000/demo.html"
    
    print(f"Opening demo interface: {demo_url}")
    webbrowser.open(demo_url)

def main():
    """Main function to start the demo"""
    print("Starting Domain-Specific FAQ Chatbot Demo")
    print("----------------------------------------")
    
    # Check if the server is already running
    try:
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("Server is already running.")
            server_process = None
        else:
            server_process = start_server()
    except requests.exceptions.ConnectionError:
        server_process = start_server()
    
    # Open the demo interface
    open_demo()
    
    if server_process:
        print("\nServer is running. Press Ctrl+C to stop the demo.")
        try:
            # Keep the script running until interrupted
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping the server...")
            # Kill the server process
            if platform.system() == 'Windows':
                server_process.terminate()
            else:
                try:
                    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
                except AttributeError:
                    server_process.terminate()
            print("Server stopped.")
    else:
        print("\nDemo is running with an existing server instance.")
        print("Close your browser when done.")

if __name__ == "__main__":
    main() 