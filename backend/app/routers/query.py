from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from fastapi.responses import JSONResponse

from backend.app.services.db import NeonDBClient
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.qdrant_client import QdrantVectorStore
from backend.app.services.retrieval import RetrievalService # Will be created later
from backend.app.dependencies import get_db_client, get_qdrant_vector_store # Import dependency functions

router = APIRouter()

# Dependency to get RetrievalService instance
async def get_retrieval_service(
    db_client: NeonDBClient = Depends(get_db_client),
    embed_service: EmbeddingService = Depends(EmbeddingService),
    
    qdrant_vector_store: QdrantVectorStore = Depends(get_qdrant_vector_store)
):
    # await db_client.connect() # connect is handled in main.py startup event
    return RetrievalService(db_client=db_client, embedding_service=embed_service, qdrant_client=qdrant_vector_store)
    
class QueryRequest(BaseModel):
    user_query: str
    selected_text: Optional[str] = None # For selected-text only query mode (FR-007)

@router.post("/", summary="Retrieve relevant chunks based on user query")
async def query_chunks(
    request: QueryRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
) -> List[Dict[str, Any]]:
    """
    Accepts a user query and optional selected text, then retrieves and returns
    relevant chunks from Qdrant and Neon Postgres.
    """
    try:    
        # T083: Implement query logic using retrieval_service
        # T086: Incorporate selected text for contextual filtering
        retrieved_chunks = await retrieval_service.retrieve_chunks(
            user_query=request.user_query,
            selected_text=request.selected_text
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[chunk for chunk in retrieved_chunks]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}"
        )
