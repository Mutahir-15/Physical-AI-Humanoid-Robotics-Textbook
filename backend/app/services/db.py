import os
import asyncpg
import uuid
import datetime
from typing import List, Dict, Any, Optional

class NeonDBClient:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set.")
        self.conn_pool = None

    async def connect(self):
        """Initializes the connection pool."""
        if not self.conn_pool:
            self.conn_pool = await asyncpg.create_pool(self.database_url)
            print("Neon PostgreSQL connection pool created.")

    async def close(self):
        """Closes the connection pool."""
        if self.conn_pool:
            await self.conn_pool.close()
            self.conn_pool = None
            print("Neon PostgreSQL connection pool closed.")

    async def _execute(self, query: str, *args):
        """Helper to execute a query and return results."""
        if not self.conn_pool:
            await self.connect()
        async with self.conn_pool.acquire() as connection:
            return await connection.fetch(query, *args)

    def _record_to_dict(self, record: asyncpg.Record) -> Dict[str, Any]:
        """Converts an asyncpg.Record to a dictionary, converting UUIDs and datetimes to strings."""
        converted_record = {}
        for key, value in record.items():
            if isinstance(value, uuid.UUID):
                converted_record[key] = str(value)
            elif isinstance(value, datetime.datetime):
                converted_record[key] = value.isoformat()
            else:
                converted_record[key] = value
        return converted_record

    async def initialize_schema(self):
        """Executes the schema.sql to create necessary tables."""
        schema_file_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'schema.sql')
        try:
            with open(schema_file_path, 'r') as f:
                schema_sql = f.read()

            commands = [cmd.strip() for cmd in schema_sql.split(';') if cmd.strip()]
            async with self.conn_pool.acquire() as connection:
                for command in commands:
                    await connection.execute(command)
            print("Database schema initialized successfully.")
        except Exception as e:
            print(f"Error initializing database schema: {e}")
            raise

    async def insert_chunk_metadata(self, metadata: Dict[str, Any]) -> Optional[str]:
        """
        Inserts metadata for a single chunk into the 'chunks' table.
        If the chunk_id already exists, it does nothing.
        Returns the generated UUID of the chunk if inserted, otherwise None.
        """
        query = """
            INSERT INTO chunks (chunk_id, source_path, chapter, section, text_content, token_count, start_position, end_position)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (chunk_id) DO NOTHING
            RETURNING id;
        """
        result = await self._execute(
            query,
            metadata['chunk_id'], metadata['source_path'], metadata.get('chapter'),
            metadata.get('section'), metadata['text_content'], metadata['token_count'],
            metadata.get('start_position'), metadata.get('end_position')
        )
        return str(result[0]['id']) if result else None

    async def get_chunk_metadata_by_id(self, chunk_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves chunk metadata by its UUID.
        """
        query = "SELECT * FROM chunks WHERE id = $1;"
        record = await self._execute(query, chunk_uuid)
        return self._record_to_dict(record[0]) if record else None

    async def get_chunk_metadata_by_chunk_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves chunk metadata by its unique chunk_id.
        """
        query = "SELECT * FROM chunks WHERE chunk_id = $1;"
        record = await self._execute(query, chunk_id)
        return self._record_to_dict(record[0]) if record else None
    
    async def get_chunks_by_source_path(self, source_path: str) -> List[Dict[str, Any]]:
        """
        Retrieves all chunk metadata associated with a given source file path.
        """
        query = "SELECT * FROM chunks WHERE source_path = $1 ORDER BY start_position;"
        records = await self._execute(query, source_path)
        return [self._record_to_dict(r) for r in records]

    async def delete_chunks_by_source_path(self, source_path: str):
        """
        Deletes all chunk metadata associated with a given source file path.
        """
        query = "DELETE FROM chunks WHERE source_path = $1;"
        await self._execute(query, source_path)
        print(f"Deleted chunks for source_path: {source_path}")

    async def update_chunk_metadata(self, chunk_id: str, updates: Dict[str, Any]):
        """
        Updates metadata for an existing chunk based on chunk_id.
        """
        set_clauses = [f"{key} = ${i+2}" for i, key in enumerate(updates.keys())]
        query = f"""
            UPDATE chunks
            SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP
            WHERE chunk_id = $1;
        """
        values = [chunk_id] + list(updates.values())
        await self._execute(query, *values)
        print(f"Updated metadata for chunk_id: {chunk_id}")

