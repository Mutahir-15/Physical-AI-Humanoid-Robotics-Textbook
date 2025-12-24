from fastapi import Depends
from backend.app.services.db import NeonDBClient
from backend.app.services.qdrant_client import QdrantVectorStore

# --- Database Client (T071 initial connection) ---
db_client = NeonDBClient()

# --- Qdrant Vector Store (T077 initial connection) ---
qdrant_vector_store = QdrantVectorStore()

# Dependency to provide DB client to routes
async def get_db_client():
    return db_client

# Dependency to provide QdrantVectorStore client to routes
async def get_qdrant_vector_store():
    return qdrant_vector_store