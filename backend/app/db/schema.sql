CREATE TABLE IF NOT EXISTS chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id TEXT UNIQUE NOT NULL,       -- Unique identifier for the chunk (e.g., hash of content + source)
    source_path TEXT NOT NULL,           -- Path to the original MDX file
    chapter TEXT,                        -- Extracted chapter title from MDX frontmatter/headers
    section TEXT,                        -- Extracted section title
    text_content TEXT NOT NULL,          -- The actual text content of the chunk
    token_count INTEGER NOT NULL,        -- Number of tokens in the chunk (using Cohere's tokenizer)
    start_position INTEGER,              -- Starting character position of the chunk in the original document
    end_position INTEGER,                -- Ending character position
    embedding_vector_id UUID,            -- Foreign key to Qdrant if separate ID used, or just logical link
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index on source_path for efficient retrieval of chunks by document
CREATE INDEX IF NOT EXISTS idx_chunks_source_path ON chunks (source_path);

-- Index on chapter and section for hierarchical content retrieval
CREATE INDEX IF NOT EXISTS idx_chunks_chapter_section ON chunks (chapter, section);

-- Optional: For tracking versions of source documents
CREATE TABLE IF NOT EXISTS document_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_path TEXT UNIQUE NOT NULL,    -- Path to the original MDX file
    last_ingested_hash TEXT NOT NULL,    -- Hash of the document content at last ingestion
    last_ingested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);