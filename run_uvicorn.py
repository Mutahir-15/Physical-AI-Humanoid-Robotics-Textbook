import subprocess
import sys
from dotenv import load_dotenv

load_dotenv('backend/.env')  # Load environment variables from .env file



# Construct the uvicorn command
uvicorn_command = [
    sys.executable,
    "-m",
    "uvicorn",
    "backend.app.main:app",
    "--reload",
    "--port",
    "8000"
]

# Run the uvicorn command as a subprocess
try:
    subprocess.run(uvicorn_command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running uvicorn: {e}")
    sys.exit(1)
