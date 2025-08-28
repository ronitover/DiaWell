#!/usr/bin/env python3
"""
Alternative start script for the Diabetes Risk Assessment API.
Uses the module approach for better compatibility across systems.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Start the API server using uvicorn module approach."""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    print("🚀 Starting Diabetes Risk Assessment API...")
    print(f"📍 Working directory: {script_dir}")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to the script directory
        os.chdir(script_dir)
        
        # Start the server using uvicorn module
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
