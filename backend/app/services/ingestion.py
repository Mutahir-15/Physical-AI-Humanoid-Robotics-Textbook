import os
import uuid
from typing import List, Dict, Any
from pathlib import Path

from backend.app.services.db import NeonDBClient
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.qdrant_client import QdrantVectorStore
from backend.src.utils.content_cleaner import clean_mdx_content
from backend.src.utils.mdx_chunker import chunk_mdx_content

BATCH_SIZE = 100  # Batch size for upserting to Qdrant

class IngestionService:
    def __init__(self, db_client: NeonDBClient, embedding_service: EmbeddingService, qdrant_client: QdrantVectorStore):
        self.db_client = db_client
        self.embedding_service = embedding_service
        self.qdrant_client = qdrant_client
        self.docs_directory = os.getenv("DOCS_DIRECTORY", "docs")

    async def ingest_all_docs(self) -> Dict[str, Any]:
        """Ingests all MDX documents from the configured docs_directory."""
        mdx_files = list(Path(self.docs_directory).rglob("*.mdx"))
        file_paths = [str(f) for f in mdx_files]
        return await self.ingest_files(file_paths)

    async def ingest_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Ingests a list of specified MDX files."""
        ingested_count = 0
        failed_files = []
        namespace_uuid = uuid.NAMESPACE_DNS

        for file_path_str in file_paths:
            try:
                file_path = Path(file_path_str)
                with open(file_path, 'r', encoding='utf-8') as f:
                    mdx_content = f.read()

                cleaned_content = clean_mdx_content(mdx_content)
                chunks_data = chunk_mdx_content(cleaned_content, chunk_size=550, chunk_overlap=50)
                texts_to_embed = [chunk['text_content'] for chunk in chunks_data]
                
                # Generate embeddings for all chunks of the file at once
                all_embeddings = await self.embedding_service.generate_embeddings(texts_to_embed)

                qdrant_ids = []
                qdrant_payloads = []
                neon_metadatas = []

                for i, chunk in enumerate(chunks_data):
                    unique_chunk_id = str(uuid.uuid5(namespace_uuid, f"{file_path.name}-{i}"))
                    
                    qdrant_ids.append(unique_chunk_id)
                    payload = chunk['metadata'].copy()
                    payload["chunk_id"] = unique_chunk_id
                    payload["text_content"] = chunk["text_content"]
                    payload["source_path"] = str(file_path)
                    qdrant_payloads.append(payload)

                    neon_metadatas.append({
                        "chunk_id": unique_chunk_id,
                        "source_path": str(file_path),
                        "chapter": chunk["metadata"].get("chapter"),
                        "section": chunk["metadata"].get("section"),
                        "text_content": chunk["text_content"],
                        "token_count": chunk["metadata"].get("token_count"),
                        "start_position": chunk["metadata"].get("start_position", 0),
                        "end_position": chunk["metadata"].get("end_position", 0)
                    })
                
                # Process in batches
                for i in range(0, len(qdrant_ids), BATCH_SIZE):
                    batch_ids = qdrant_ids[i:i + BATCH_SIZE]
                    batch_embeddings = all_embeddings[i:i + BATCH_SIZE]
                    batch_payloads = qdrant_payloads[i:i + BATCH_SIZE]
                    batch_neon_metadatas = neon_metadatas[i:i + BATCH_SIZE]

                    # Upsert to Qdrant in batches
                    await self.qdrant_client.upsert_vectors(batch_ids, batch_embeddings, batch_payloads)
                    
                    # Insert into Neon Postgres in batches
                    for metadata_item in batch_neon_metadatas:
                        await self.db_client.insert_chunk_metadata(metadata_item)

                ingested_count += 1
                print(f"Successfully ingested {file_path_str}")

            except Exception as e:
                failed_files.append({"file": file_path_str, "error": str(e)})
                print(f"Failed to ingest {file_path_str}: {e}")

        return {
            "ingested_count": ingested_count,
            "failed_count": len(failed_files),
            "failed_files": failed_files
        }
