from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from backend.app.services.db import NeonDBClient
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.qdrant_client import QdrantVectorStore

class RetrievalService:
    def __init__(self, db_client: NeonDBClient, embedding_service: EmbeddingService, qdrant_client: QdrantVectorStore):
        self.db_client = db_client
        self.embedding_service = embedding_service
        self.qdrant_client = qdrant_client

    async def retrieve_chunks(self, user_query: str, selected_text: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves relevant chunks from Qdrant and Neon Postgres based on the user query
        and optional selected text.
        """
        query_text = selected_text if selected_text else user_query
        if not query_text:
            return []

        # 1. Generate embedding for the query
        query_embedding = (await self.embedding_service.generate_embeddings([query_text], input_type="search_query"))[0]


        # 2. Search Qdrant for similar vectors (T078)
        # Apply filter if selected_text is used to prioritize chunks related to that context
        qdrant_filter = None
        # Example of how a filter could be applied based on selected_text's inferred source
        # This part requires more advanced logic to infer source from selected_text
        # For MVP, we'll keep it simple or expand later.

        search_results = await self.qdrant_client.search_vectors(query_embedding, limit=5, query_filter=qdrant_filter)

        retrieved_chunks = []
        for result in search_results:
            # 3. Fetch corresponding full chunk text and metadata from Neon Postgres (T079)
            # Qdrant payload already contains much of the metadata and text_content
            # but we can fetch full details from Postgres if needed or for consistency.
            # For this MVP, we'll primarily use payload from Qdrant if it's rich enough.
            # If `embedding_vector_id` is used as Qdrant ID, we can use that to query Postgres.
            chunk_metadata_from_db = await self.db_client.get_chunk_metadata_by_chunk_id(result['payload']['chunk_id'])
            
            if chunk_metadata_from_db:
                # Combine Qdrant payload and DB metadata, preferring DB for completeness
                full_chunk_info = {**result['payload'], **chunk_metadata_from_db}
                retrieved_chunks.append(full_chunk_info)
            else:
                retrieved_chunks.append(result['payload']) # Fallback to Qdrant payload

        # T086: Refine retrieval to incorporate selected text for contextual filtering
        # This is where more advanced re-ranking or filtering based on selected_text proximity
        # could be implemented. For now, the `query_text` selection handles the primary intent.

        return retrieved_chunks
