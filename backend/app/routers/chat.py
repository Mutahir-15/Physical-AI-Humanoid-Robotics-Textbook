from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from fastapi.responses import JSONResponse

from backend.app.services.db import NeonDBClient
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.qdrant_client import QdrantVectorStore
from backend.app.services.retrieval import RetrievalService # Will be created later
from backend.app.agents.gemini_agent import GeminiAgent # Will be created later
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

# Dependency to get GeminiAgent instance
async def get_gemini_agent():
    return GeminiAgent()


class ChatRequest(BaseModel):
    user_message: str
    chat_history: Optional[List[Dict[str, str]]] = None # For potential conversational memory
    selected_text: Optional[str] = None # For selected-text only query mode

@router.post("/", summary="Engage RAG Chatbot for grounded answer generation")
async def chat_with_rag(
    request: ChatRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
    gemini_agent: GeminiAgent = Depends(get_gemini_agent)
) -> Dict[str, Any]:
    """
    Orchestrates the RAG process: retrieves relevant chunks,
    passes them to Gemini, and returns a grounded answer.
    """
    try:
        # 1. Retrieve relevant chunks (T085)
        retrieved_chunks = await retrieval_service.retrieve_chunks(
            user_query=request.user_message,
            selected_text=request.selected_text
        )
        
        # 2. Extract text content from chunks for context
        context_texts = [chunk['text_content'] for chunk in retrieved_chunks]
        
        # 3. Generate answer using Gemini (T085)
        response_content = await gemini_agent.generate_grounded_answer(
            user_query=request.user_message,
            context_chunks=context_texts,
            chat_history=request.chat_history
        )
        
        # 4. Prepare citations (T085, based on Contextual Boundaries doc)
        citations = [
            {
                "source_path": chunk.get('source_path', 'Unknown'), 
                "chapter": chunk.get('chapter'), 
                "section": chunk.get('section')
            }
            for chunk in retrieved_chunks
        ]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"answer": response_content, "citations": citations}
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )
