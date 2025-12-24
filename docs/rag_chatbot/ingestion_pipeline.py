import os
import re
import asyncio
from typing import List, Dict, Any
from uuid import uuid4

import cohere
from qdrant_client import QdrantClient, models

# Import service clients
from backend.app.services.ingestion.content_cleaner import clean_mdx_content
from backend.app.services.ingestion.mdx_chunker import chunk_mdx_content, get_token_count
from backend.app.services.db import NeonDBClient # Import NeonDBClient

# --- Configuration ---
DOCS_DIR = "../../docs" # Relative path to the docs directory
CHUNK_SIZE = 750
CHUNK_OVERLAP = 100

# Cohere and Qdrant API settings (placeholders)
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "YOUR_COHERE_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST", "YOUR_QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "YOUR_QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = "rag_chunks"

# --- Utility Functions ---

def extract_metadata_from_path(file_path: str) -> Dict[str, str]:
    """
    Extracts chapter and section information from the file path.
    Assumes a structure like docs/moduleX-name/chapterY-name-title.mdx
    """
    parts = file_path.split(os.sep)
    chapter = "Unknown Chapter"
    section = "Unknown Section" # This will be derived later from chunk content or actual headings

    if len(parts) >= 3 and parts[-3].startswith("module"):
        chapter = parts[-2].replace("-", " ").replace(".mdx", "").title()
        # Attempt to get a more specific section if chapter is a full path segment
        if "chapter" in parts[-1]:
            section = parts[-1].replace("-", " ").replace(".mdx", "").title()
        else:
            section = chapter # Fallback if specific chapter part isn't clear
    elif len(parts) >= 2: # For simpler structures like docs/chapter-name.mdx
        chapter = parts[-1].replace("-", " ").replace(".mdx", "").title()
        section = chapter
        
    return {"chapter": chapter, "section": section}

# --- Main Ingestion Pipeline ---

async def run_ingestion_pipeline(): # Made async
    all_chunks_with_metadata: List[Dict[str, Any]] = []

    # 1. Load and Process Content
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".mdx"):
                file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(file_path, DOCS_DIR)

                print(f"Processing {relative_file_path}...")
                with open(file_path, "r", encoding="utf-8") as f:
                    mdx_content = f.read()

                cleaned_content = clean_mdx_content(mdx_content)
                path_metadata = extract_metadata_from_path(relative_file_path)

                # 2. Apply Chunking Strategy
                processed_chunks = chunk_mdx_content(
                    cleaned_content,
                    max_tokens=CHUNK_SIZE,
                    overlap_tokens=CHUNK_OVERLAP,
                    file_metadata=path_metadata
                )

                for chunk_data_from_chunker in processed_chunks:
                    # 3. Prepare for Embedding
                    chunk_id = str(uuid4()) # Generate a unique ID for each chunk
                    
                    chunk_data = {
                        "id": chunk_id,
                        "chunk_text": chunk_data_from_chunker["text_content"],
                        "source_path": relative_file_path,
                        "chapter": chunk_data_from_chunker["metadata"].get("chapter", path_metadata["chapter"]),
                        "section": chunk_data_from_chunker["metadata"].get("section", path_metadata["section"]),
                        "token_count": chunk_data_from_chunker["token_count"],
                        "metadata": {
                            **chunk_data_from_chunker["metadata"],
                        }
                    }
                    all_chunks_with_metadata.append(chunk_data)

    print(f"\nPrepared {len(all_chunks_with_metadata)} chunks for ingestion.")

    # 4. Generate Embeddings using Cohere API
    co = cohere.Client(COHERE_API_KEY)
    for chunk_data in all_chunks_with_metadata:
        try:
            response = co.embed(
                texts=[chunk_data["chunk_text"]],
                model="embed-english-v3.0",
                input_type="search_document"
            )
            chunk_data["embedding_vector"] = response.embeddings[0]
        except Exception as e:
            print(f"Error generating embedding for chunk {chunk_data['id']}: {e}")
            chunk_data["embedding_vector"] = []

    print(f"Embeddings generated for {len(all_chunks_with_metadata)} chunks.")

    # 5. Store Vectors in Qdrant Cloud Free Tier
    qdrant_client_instance = QdrantClient(host=QDRANT_HOST, api_key=QDRANT_API_KEY)
    
    try:
        qdrant_client_instance.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists. Skipping recreation.")
    except Exception:
        qdrant_client_instance.recreate_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
            on_disk_payload=True
        )
        print(f"Collection '{QDRANT_COLLECTION_NAME}' created.")
    
    points = []
    for chunk_data in all_chunks_with_metadata:
        payload = {k: v for k, v in chunk_data.items() if k not in ["embedding_vector", "chunk_text", "id"]}
        payload["chunk_id"] = chunk_data["id"]
        payload["text_content"] = chunk_data["chunk_text"]
        payload["text_content_preview"] = chunk_data["chunk_text"][:200] + "..."
        
        if not chunk_data["embedding_vector"]:
            print(f"Skipping chunk {chunk_data['id']} due to empty embedding vector.")
            continue

        points.append(
            models.PointStruct(
                id=chunk_data["id"],
                vector=chunk_data["embedding_vector"],
                payload=payload
            )
        )
    
    if points:
        qdrant_client_instance.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            wait=True,
            points=points
        )
        print(f"Qdrant storage: Upserted {len(points)} points into '{QDRANT_COLLECTION_NAME}'.")
    else:
        print("No points to upsert into Qdrant.")

    # 5. Store Metadata in Neon Postgres
    db_client = None
    try:
        db_client = NeonDBClient()
        await db_client.connect()
        # Schema initialization is generally done once, but calling it here ensures it's ready.
        # In a real application, you might want to manage schema creation separately.
        await db_client.initialize_schema() 

        for i, chunk_data in enumerate(all_chunks_with_metadata):
            pg_metadata = {
                "chunk_id": chunk_data["id"],
                "source_path": chunk_data["source_path"],
                "chapter": chunk_data["chapter"],
                "section": chunk_data["section"],
                "text_content": chunk_data["chunk_text"],
                "token_count": chunk_data["token_count"],
                "start_position": chunk_data["metadata"].get("start_position"),
                "end_position": chunk_data["metadata"].get("end_position"),
            }
            await db_client.insert_chunk_metadata(pg_metadata)
            if (i + 1) % 100 == 0:
                print(f"Inserted {i + 1}/{len(all_chunks_with_metadata)} chunks into Neon Postgres.")
        print(f"Successfully inserted {len(all_chunks_with_metadata)} chunks into Neon Postgres.")

    except Exception as e:
        print(f"Error storing metadata in Neon Postgres: {e}")
    finally:
        if db_client:
            await db_client.close()

    print("\nIngestion pipeline completed.")

if __name__ == "__main__":
    asyncio.run(run_ingestion_pipeline())
