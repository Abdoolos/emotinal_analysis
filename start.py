import os
import subprocess
import sys
import time
import webbrowser
from threading import Thread

def install_backend():
    print("Installing backend dependencies...")
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    requirements_path = os.path.join(backend_dir, "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print(f"Error: Could not find {requirements_path}")
        return False
        
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing backend dependencies: {e}")
        return False

def install_frontend():
    print("Installing frontend dependencies...")
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    
    if not os.path.exists(frontend_dir):
        print(f"Error: Could not find {frontend_dir}")
        return False
        
    try:
        os.chdir(frontend_dir)
        if os.name == 'nt':  # Windows
            subprocess.run(["npm.cmd", "install"], check=True)
        else:  # Unix/Linux/MacOS
            subprocess.run(["npm", "install"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing frontend dependencies: {e}")
        return False
    finally:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_backend():
    print("Starting backend server...")
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_src = os.path.join(project_root, "backend", "src")
    
    if not os.path.exists(backend_src):
        print(f"Error: Could not find {backend_src}")
        return
        
    current_dir = os.getcwd()
    try:
        os.chdir(backend_src)
        try:
            subprocess.run([
                sys.executable, "-m", "uvicorn", 
                "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error starting backend server: {e}")
        except KeyboardInterrupt:
            print("\nStopping backend server...")
    finally:
        os.chdir(current_dir)

def run_frontend():
    print("Starting frontend server...")
    project_root = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(project_root, "frontend")
    
    if not os.path.exists(frontend_dir):
        print(f"Error: Could not find {frontend_dir}")
        return
        
    current_dir = os.getcwd()
    try:
        os.chdir(frontend_dir)
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(["npm.cmd", "start"])
            else:  # Unix/Linux/MacOS
                subprocess.run(["npm", "start"])
        except KeyboardInterrupt:
            print("\nStopping frontend server...")
    finally:
        os.chdir(current_dir)

def open_browser():
    time.sleep(5)  # Wait for servers to start
    print("Opening application in browser...")
    webbrowser.open('http://localhost:3000')

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"Project root: {project_root}")
    
    try:
        # Check if we're in a virtual environment
        if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
            print("Warning: Not running in a virtual environment!")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return

        # Start backend in a separate thread
        print("\nStarting servers...")
        backend_thread = Thread(target=run_backend)
        backend_thread.daemon = True
        backend_thread.start()

        # Wait a bit for backend to initialize
        time.sleep(2)

        # Start frontend in a separate thread
        frontend_thread = Thread(target=run_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()

        # Open browser after both servers have started
        browser_thread = Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Keep the main thread running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down servers...")

if __name__ == "__main__":
    print("""
╭──────────────────────────────────────────╮
│    نظام تحليل المشاعر - Emotion Detection    │
│    المصمم: عبدالله العويس                   │
╰──────────────────────────────────────────╯
    """)
    main()
