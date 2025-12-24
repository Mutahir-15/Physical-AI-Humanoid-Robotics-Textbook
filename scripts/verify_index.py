import os
import asyncio
from dotenv import load_dotenv

from backend.app.services.qdrant_client import QdrantVectorStore
from backend.app.services.db import NeonDBClient

# Load environment variables
load_dotenv()

async def verify_qdrant_and_neon_index():
    print("Verifying Qdrant and Neon Postgres index...")
    
    qdrant_client = QdrantVectorStore()
    neon_db_client = NeonDBClient()
    
    try:
        await neon_db_client.connect()
        await neon_db_client.initialize_schema() # Ensure schema is up
        
        # Verify Qdrant collection exists and has some points
        collection_info = await qdrant_client.client.get_collection(qdrant_client.collection_name)
        print(f"Qdrant collection '{qdrant_client.collection_name}' info: {collection_info.points_count} points, status: {collection_info.status}")
        
        if collection_info.points_count == 0:
            print("Warning: Qdrant collection is empty. Run ingestion first.")
            return False

        # Verify Neon DB has some chunks
        # This is a simple count, you might want more sophisticated checks
        async with neon_db_client.conn_pool.acquire() as connection:
            record_count = await connection.fetchval("SELECT COUNT(*) FROM chunks;")
        print(f"Neon Postgres 'chunks' table has {record_count} records.")

        if record_count == 0:
            print("Warning: Neon Postgres 'chunks' table is empty. Run ingestion first.")
            return False
            
        print("Index verification successful: Qdrant and Neon Postgres contain data.")
        return True

    except Exception as e:
        print(f"Error during index verification: {e}")
        return False
    finally:
        await neon_db_client.close()

if __name__ == "__main__":
    asyncio.run(verify_qdrant_and_neon_index())
