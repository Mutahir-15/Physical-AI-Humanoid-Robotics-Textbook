    # Feature Specification: RAG Chatbot Integration for Docusaurus Book (Free Stack)

**Feature Branch**: `001-rag-chatbot-docusaurus`  
**Created**: 2025-12-10  
**Status**: Draft  
**Input**: User description: "Title: RAG Chatbot Integration for Docusaurus Book (Free Stack) Objective: Build a Retrieval-Augmented Generation (RAG) chatbot for the live Docusaurus robotics book using FREE-tier services: Gemini API (LLM), Cohere Embed v3 (embeddings), Qdrant Cloud (vectors), Neon Serverless Postgres (metadata), FastAPI backend, and ChatKit or lightweight Streamlit UI embedded into the book. Non-Functional Requirements: - All services must operate in free-tier limits - Typical response latency under ~2s (after retrieval) - Modular code (services/, routers/, db/, utils/) - Environment variables only for secrets - Logging of ingest/query/chat - Tests: basic unit and integration Acceptance Criteria: - At least 98% of book content ingested and indexed - Chat widget visible on every page - User-selected-text → accurate answer flow works - Backend reachable and stable on free-tier host - Answering is grounded to retrieved content (no hallucinations) Constraints: - Must use Cohere for embeddings, Qdrant for vectors, Neon for metadata, Gemini for LLM - No paid services required to prototype & demo - Integrate into current Docusaurus deployment Deliverable summary: - Spec doc + plan + executable tasks - Ingestion scripts, embedding pipeline, Qdrant index, Neon schema - FastAPI backend with endpoints - Chat widget UI integrated into Docusaurus - Deployment scripts and docs End."

## Summary

Build a Retrieval-Augmented Generation (RAG) chatbot for the live Docusaurus robotics book using FREE-tier services: Gemini API (LLM), Cohere Embed v3 (embeddings), Qdrant Cloud (vectors), Neon Serverless Postgres (metadata), FastAPI backend, and ChatKit or lightweight Streamlit UI embedded into the book.

## Clarifications

### Session 2025-12-10

- Q: Which tokenizer should be used for measuring tokens during chunking? → A: Cohere's tokenizer (used by `embed-english-v3.0`).
- Q: Which specific Gemini model (e.g., `gemini-pro`, `gemini-2.5-flash`) should be used for reasoning? → A: `gemini-2.5-flash`.
- Q: What authentication/authorization mechanism should be enforced for the `/ingest` endpoint? → A: API Key specific to ingestion.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Question & Get Grounded Answer (Priority: P1)

As a user of the Docusaurus robotics book, I want to ask questions about the book's content through a chat widget and receive accurate, relevant answers that are strictly derived from the book's information.

**Why this priority**: This is the core functionality and primary value proposition of the RAG chatbot.

**Independent Test**: Can be fully tested by asking a question about a specific topic from the book and verifying the answer's accuracy and grounding in the text.

**Acceptance Scenarios**:

1.  **Given** I am on any page of the Docusaurus book, **When** I open the chat widget and ask "What are ROS 2 nodes?", **Then** I receive a concise answer based on the book's definition of ROS 2 nodes.
2.  **Given** I ask a question whose answer is not in the book, **When** I ask "What is the current weather in London?", **Then** the chatbot informs me that it can only answer questions related to the book's content.

### User Story 2 - Ingest New/Updated Content (Priority: P1)

As a content administrator, I want to easily ingest new or updated MDX documents into the RAG system so that the chatbot's knowledge base remains current.

**Why this priority**: Essential for maintaining an up-to-date and comprehensive knowledge base for the chatbot.

**Independent Test**: Can be fully tested by adding a new MDX file to the `docs/` directory and verifying its ingestion via the `/ingest` endpoint and subsequent retrievability by the chatbot.

**Acceptance Scenarios**:

1.  **Given** a new `.mdx` file is added to the `docs/` directory, **When** the `/ingest` endpoint is called, **Then** the new content is processed, chunked, embedded, and stored in Qdrant and Neon Postgres.
2.  **Given** an existing `.mdx` file is updated, **When** the `/ingest` endpoint is called, **Then** the updated content replaces the old content in the RAG system, and the chatbot reflects the changes.

### User Story 3 - Query Selected Text (Priority: P2)

As a user, I want to select a specific passage of text within the Docusaurus book and ask the chatbot a question related to only that selected text to get focused information.

**Why this priority**: Enhances user experience by providing more targeted context to the chatbot.

**Independent Test**: Can be tested by selecting a paragraph, querying the chatbot about it, and ensuring the response is based only on the selected text.

**Acceptance Scenarios**:

1.  **Given** I select a paragraph of text on a book page, **When** I use a "query selected text" feature in the chat widget and ask "Summarize this", **Then** the chatbot provides a summary strictly based on the selected text.

### User Story 4 - Backend Health Monitoring (Priority: P3)

As a system operator, I want to check the health status of the RAG chatbot backend to ensure it is operational.

**Why this priority**: Basic operational readiness.

**Independent Test**: Can be tested by hitting the `/health` endpoint and expecting a successful response.

**Acceptance Scenarios**:

1.  **Given** the backend service is running, **When** a `GET` request is sent to `/health`, **Then** a 200 OK response is returned.

### Edge Cases

- What happens when the `docs/` directory is empty or contains malformed MDX files during ingestion? (Should gracefully handle, log errors, skip invalid files)
- How does the system handle high concurrent query loads within free-tier limits? (Graceful degradation, rate-limiting)
- What happens if Cohere/Qdrant/Gemini APIs are down or return errors during ingestion/query? (Robust error handling, retry mechanisms, informative user messages)

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST ingest `.mdx` documents from the `docs/` directory, clean their content, chunk them (300-600 tokens with overlap, measured using **Cohere's tokenizer**), create embeddings using Cohere, and store vectors in Qdrant.
-   **FR-002**: The system MUST store metadata (source file, chapter, chunk_id, start_pos) in Neon Serverless Postgres for each ingested chunk.
-   **FR-003**: The backend MUST expose a `POST /ingest` endpoint to trigger the content ingestion pipeline.
-   **FR-004**: The backend MUST expose a `POST /query` endpoint that accepts a user query and optional selected text, retrieves relevant chunks from Qdrant/Neon, and passes them to the LLM.
-   **FR-005**: The backend MUST expose a `POST /chat` endpoint that orchestrates the RAG process, using the **`gemini-2.5-flash`** model of the Gemini API for reasoning and answer generation, strictly grounded in retrieved context.
-   **FR-006**: The backend MUST expose a `GET /health` endpoint to report its operational status.
-   **FR-007**: The system MUST support a "selected-text only" query mode, where the chatbot's response is solely based on the provided selected text and relevant retrieved context.
-   **FR-008**: The frontend MUST embed a chat widget (using ChatKit or Streamlit iframe) across all Docusaurus book pages.

### Key Entities *(include if feature involves data)*

-   **Document**: An original `.mdx` file from the Docusaurus `docs/` directory.
-   **Chunk**: A semantically coherent segment of text derived from a Document, used for embedding and retrieval.
    *   Attributes: `id`, `text_content`, `source_path`, `chapter`, `section`, `token_count`, `embedding_vector`, `start_position` (in original doc).
-   **User Query**: The question or selected text provided by the user.
-   **Chatbot Response**: The answer generated by the LLM based on retrieved context.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: At least 98% of the `.mdx` content from the `docs/` directory is successfully ingested and indexed within the free-tier service limits.
-   **SC-002**: The chat widget is visibly present and interactive on all pages of the Docusaurus book.
-   **SC-003**: The "User-selected-text → accurate answer" flow consistently works, providing grounded answers within the context of the selected text and retrieved documents.
-   **SC-004**: The backend API endpoints (`/ingest`, `/query`, `/chat`, `/health`) are reachable and stable when deployed on free-tier hosting.
-   **SC-005**: The chatbot's answers are consistently grounded in the retrieved content, with a hallucination rate of less than 2% during testing.
-   **SC-006**: Typical response latency for `/chat` and `/query` endpoints is under 2 seconds (after document retrieval latency) for average user queries within free-tier resource constraints.

### User Story 1 - Ask Question & Get Grounded Answer (Priority: P1)

As a user of the Docusaurus robotics book, I want to ask questions about the book's content through a chat widget and receive accurate, relevant answers that are strictly derived from the book's information.

**Why this priority**: This is the core functionality and primary value proposition of the RAG chatbot.

**Independent Test**: Can be fully tested by asking a question about a specific topic from the book and verifying the answer's accuracy and grounding in the text.

**Acceptance Scenarios**:

1.  **Given** I am on any page of the Docusaurus book, **When** I open the chat widget and ask "What are ROS 2 nodes?", **Then** I receive a concise answer based on the book's definition of ROS 2 nodes.
2.  **Given** I ask a question whose answer is not in the book, **When** I ask "What is the current weather in London?", **Then** the chatbot informs me that it can only answer questions related to the book's content.

### User Story 2 - Ingest New/Updated Content (Priority: P1)

As a content administrator, I want to easily ingest new or updated MDX documents into the RAG system so that the chatbot's knowledge base remains current.

**Why this priority**: Essential for maintaining an up-to-date and comprehensive knowledge base for the chatbot.

**Independent Test**: Can be fully tested by adding a new MDX file to the `docs/` directory and verifying its ingestion via the `/ingest` endpoint and subsequent retrievability by the chatbot.

**Acceptance Scenarios**:

1.  **Given** a new `.mdx` file is added to the `docs/` directory, **When** the `/ingest` endpoint is called, **Then** the new content is processed, chunked, embedded, and stored in Qdrant and Neon Postgres.
2.  **Given** an existing `.mdx` file is updated, **When** the `/ingest` endpoint is called, **Then** the updated content replaces the old content in the RAG system, and the chatbot reflects the changes.

### User Story 3 - Query Selected Text (Priority: P2)

As a user, I want to select a specific passage of text within the Docusaurus book and ask the chatbot a question related to only that selected text to get focused information.

**Why this priority**: Enhances user experience by providing more targeted context to the chatbot.

**Independent Test**: Can be tested by selecting a paragraph, querying the chatbot about it, and ensuring the response is based only on the selected text.

**Acceptance Scenarios**:

1.  **Given** I select a paragraph of text on a book page, **When** I use a "query selected text" feature in the chat widget and ask "Summarize this", **Then** the chatbot provides a summary strictly based on the selected text.

### User Story 4 - Backend Health Monitoring (Priority: P3)

As a system operator, I want to check the health status of the RAG chatbot backend to ensure it is operational.

**Why this priority**: Basic operational readiness.

**Independent Test**: Can be tested by hitting the `/health` endpoint and expecting a successful response.

**Acceptance Scenarios**:

1.  **Given** the backend service is running, **When** a `GET` request is sent to `/health`, **Then** a 200 OK response is returned.

### Edge Cases

- What happens when the `docs/` directory is empty or contains malformed MDX files during ingestion? (Should gracefully handle, log errors, skip invalid files)
- How does the system handle high concurrent query loads within free-tier limits? (Graceful degradation, rate-limiting)
- What happens if Cohere/Qdrant/Gemini APIs are down or return errors during ingestion/query? (Robust error handling, retry mechanisms, informative user messages)

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST ingest `.mdx` documents from the `docs/` directory, clean their content, chunk them (300-600 tokens with overlap), create embeddings using Cohere, and store vectors in Qdrant.
-   **FR-002**: The system MUST store metadata (source file, chapter, chunk\_id, start\_pos) in Neon Serverless Postgres for each ingested chunk.
-   **FR-003**: The backend MUST expose a `POST /ingest` endpoint to trigger the content ingestion pipeline.
-   **FR-004**: The backend MUST expose a `POST /query` endpoint that accepts a user query and optional selected text, retrieves relevant chunks from Qdrant/Neon, and passes them to the LLM.
-   **FR-005**: The backend MUST expose a `POST /chat` endpoint that orchestrates the RAG process, using the **`gemini-2.5-flash`** model of the Gemini API for reasoning and answer generation, strictly grounded in retrieved context.
-   **FR-006**: The backend MUST expose a `GET /health` endpoint to report its operational status.
-   **FR-007**: The system MUST support a "selected-text only" query mode, where the chatbot's response is solely based on the provided selected text and relevant retrieved context.
-   **FR-008**: The frontend MUST embed a chat widget (using ChatKit or Streamlit iframe) across all Docusaurus book pages.

### Key Entities *(include if feature involves data)*

-   **Document**: An original `.mdx` file from the Docusaurus `docs/` directory.
-   **Chunk**: A semantically coherent segment of text derived from a Document, used for embedding and retrieval.
    *   Attributes: `id`, `text_content`, `source_path`, `chapter`, `section`, `token_count`, `embedding_vector`, `start_position` (in original doc).
-   **User Query**: The question or selected text provided by the user.
-   **Chatbot Response**: The answer generated by the LLM based on retrieved context.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: At least 98% of the `.mdx` content from the `docs/` directory is successfully ingested and indexed within the free-tier service limits.
-   **SC-002**: The chat widget is visibly present and interactive on all pages of the Docusaurus book.
-   **SC-003**: The "User-selected-text → accurate answer" flow consistently works, providing grounded answers within the context of the selected text and retrieved documents.
-   **SC-004**: The backend API endpoints (`/ingest`, `/query`, `/chat`, `/health`) are reachable and stable when deployed on free-tier hosting.
-   **SC-005**: The chatbot's answers are consistently grounded in the retrieved content, with a hallucination rate of less than 2% during testing.
-   **SC-006**: Typical response latency for `/chat` and `/query` endpoints is under 2 seconds (after document retrieval latency) for average user queries within free-tier resource constraints.
