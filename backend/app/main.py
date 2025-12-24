from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.app.routers import ingest, query, chat, health
from backend.app.services.db import NeonDBClient
from backend.app.dependencies import db_client, qdrant_vector_store, get_db_client, get_qdrant_vector_store

# Load environment variables from .env file
load_dotenv()
if not os.getenv("DATABASE_URL"):
    load_dotenv('backend/.env')

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot Backend",
    version="0.1.0",
    description="Backend for the Docusaurus RAG Chatbot, using FastAPI, Cohere, Qdrant, and Neon Postgres."
)

# --- CORS Configuration (T088) ---
# Allow requests from the Docusaurus book domain
# In a production environment, replace "*" with your actual Docusaurus domain(s)
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"), # Default to Docusaurus dev server
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
async def startup_event():
    print("Application startup event triggered.")
    await db_client.connect()
    await qdrant_vector_store.initialize()
    # Optionally, initialize schema on startup if it doesn't exist
    # In production, schema migrations should be managed separately
    await db_client.initialize_schema() # Not calling here to avoid auto-migrations in production

@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutdown event triggered.")
    await db_client.close()

# Include routers
app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "RAG Chatbot Backend is running. Access /docs for API documentation."}


