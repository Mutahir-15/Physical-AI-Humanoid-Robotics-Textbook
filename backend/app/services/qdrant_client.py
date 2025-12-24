import os
from typing import List, Dict, Any, Optional

from qdrant_client import AsyncQdrantClient, models


class QdrantVectorStore:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")

        self.collection_name = "rag_chunks"
        self.vector_size = 1024  # Must match embedding dimension
        self.distance_metric = models.Distance.COSINE

        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError(
                "QDRANT_URL and QDRANT_API_KEY environment variables must be set."
            )

        # ASYNC client
        self.client = AsyncQdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            prefer_grpc=True,
        )

    async def _ensure_collection_exists(self) -> None:
        """
        Ensure the Qdrant collection exists.
        If not, create it with correct vector configuration.
        """
        try:
            await self.client.get_collection(collection_name=self.collection_name)
            print(f"Qdrant collection '{self.collection_name}' already exists.")
        except Exception:
            print(f"Creating Qdrant collection '{self.collection_name}'...")
            await self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=self.distance_metric,
                ),
                on_disk_payload=True,
            )
            print(f"Qdrant collection '{self.collection_name}' created.")

    async def initialize(self) -> None:
        """
        Initializes the Qdrant client and ensures the collection exists.
        """
        await self._ensure_collection_exists()

    async def upsert_vectors(
        self,
        ids: List[str],
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
    ):
        """
        Insert or update vectors with payload metadata.
        """
        if not ids:
            print("Qdrant upsert skipped: no ids provided.")
            return None

        if not (len(ids) == len(vectors) == len(payloads)):
            raise ValueError(
                f"Qdrant upsert length mismatch: "
                f"ids={len(ids)}, vectors={len(vectors)}, payloads={len(payloads)}"
            )

        points = [
            models.PointStruct(
                id=id_val,
                vector=vector,
                payload=payload,
            )
            for id_val, vector, payload in zip(ids, vectors, payloads)
        ]

        try:
            result = await self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True,
            )
            print(f"Upserted {len(points)} vectors into Qdrant.")
            return result
        except Exception as e:
            print(f"Qdrant upsert failed: {e}")
            raise

    async def search_vectors(
        self,
        query_vector: List[float],
        limit: int = 5,
        query_filter: Optional[models.Filter] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant.
        """
        try:
            results = await self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                query_filter=query_filter,
                limit=limit,
                with_payload=True,
            )
            return [
                {
                    "id": str(hit.id),
                    "score": hit.score,
                    "payload": hit.payload,
                }
                for hit in results.points
            ]

        except Exception as e:
            print(f"Qdrant search failed: {e}")
            raise