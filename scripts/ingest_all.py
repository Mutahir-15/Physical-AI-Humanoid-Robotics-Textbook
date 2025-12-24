import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
INGESTION_API_KEY = os.getenv("INGESTION_API_KEY")

if not INGESTION_API_KEY:
    print("Error: INGESTION_API_KEY not set in environment.")
    exit(1)

def trigger_ingestion():
    url = f"{BACKEND_URL}/ingest/"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "api_key": INGESTION_API_KEY,
        "file_paths": None # Ingest all docs in DOCS_DIRECTORY
    }

    print(f"Triggering ingestion at {url}...")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        print("Ingestion successful:")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error during ingestion: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")

if __name__ == "__main__":
    trigger_ingestion()
