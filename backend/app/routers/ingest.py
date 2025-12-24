from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import os
from fastapi.responses import JSONResponse

from backend.app.services.ingestion import IngestionService
from backend.app.services.db import NeonDBClient # For type hinting
from backend.app.services.embedding_service import EmbeddingService # For type hinting and passing
from backend.app.services.qdrant_client import QdrantVectorStore # For type hinting
from backend.app.dependencies import get_db_client, get_qdrant_vector_store
import os # Import os for os.getenv

router = APIRouter()

# Dependency to get IngestionService instance
async def get_ingestion_service(
    db: NeonDBClient = Depends(get_db_client),
    embed_service: EmbeddingService = Depends(EmbeddingService),
    qdrant: QdrantVectorStore = Depends(get_qdrant_vector_store)
):
    # Connections are established at application startup, so no need to call db.connect() here
    return IngestionService(db_client=db, embedding_service=embed_service, qdrant_client=qdrant)


class IngestRequest(BaseModel):
    # Optionally, allow specific file paths to be ingested
    file_paths: Optional[List[str]] = None
    # For full repo ingestion, file_paths can be None.
    # Add an API key for authentication (T089)
    api_key: str

@router.post("/", summary="Trigger content ingestion pipeline")
async def trigger_ingestion(
    request: IngestRequest,
    ingestion_service: IngestionService = Depends(get_ingestion_service)
):
    """
    Triggers the ingestion pipeline to process MDX documents.
    If `file_paths` is provided, only those files will be processed.
    Otherwise, all MDX files in the configured `docs/` directory will be ingested.
    """
    # Basic API Key Authentication (T089)
    # Replace with a more robust authentication mechanism in production
    if request.api_key != os.getenv("INGESTION_API_KEY"): # Use environment variable
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key for ingestion"
        )

    try:
        if request.file_paths:
            summary = await ingestion_service.ingest_files(request.file_paths)
        else:
            summary = await ingestion_service.ingest_all_docs()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Ingestion triggered successfully", "summary": summary}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {str(e)}"
        )
