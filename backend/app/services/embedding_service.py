import os
from cohere import Client as CohereClient
from typing import List, Dict

class EmbeddingService:
    def __init__(self):
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable not set.")
        self.cohere_client = CohereClient(self.cohere_api_key)

    async def generate_embeddings(self, texts: List[str], input_type: str = "search_document") -> List[List[float]]:
        """
        Generates embeddings for a list of texts using Cohere's API.
        input_type should be "search_document" for ingestion and "search_query" for retrieval.
        """
        if not texts:
            return []
        
        # Cohere embed-english-v3.0 is the specified model.
        # It's synchronous, so run in a thread pool executor to avoid blocking FastAPI's event loop.
        # For simplicity in this skeleton, we'll call it directly.
        # In a real app, use `run_in_threadpool` from `starlette.concurrency`
        # or `anyio.to_thread.run_sync`.
        try:
            response = self.cohere_client.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type=input_type # Use the passed input_type
            )
            return response.embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise
