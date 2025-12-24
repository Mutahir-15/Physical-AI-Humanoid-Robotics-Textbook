# Tasks for RAG Chatbot Integration for Docusaurus Book (Free Stack)

**Feature Branch**: `001-rag-chatbot-docusaurus` | **Date**: 2025-12-10 | **Plan**: specs/001-rag-chatbot-docusaurus/plan.md
**Input**: Implementation plan from `/specs/001-rag-chatbot-docusaurus/plan.md`

## Phase 0: Setup & Core Ingestion (MVP)

**Story Goal**: As a content administrator, I want to easily ingest new or updated MDX documents into the RAG system so that the chatbot's knowledge base remains current.
**Independent Test**: Can be fully tested by adding a new MDX file to the `docs/` directory and verifying its ingestion via the `/ingest` endpoint and subsequent retrievability by the chatbot.

- [X] T065 [US2] Install Python 3.11+ environment and create a virtual environment.
- [X] T066 [US2] Install primary dependencies: FastAPI, Uvicorn, Langchain, Cohere Python SDK, Qdrant Client, Psycopg2 (or asyncpg).
- [X] T067 [US2] Create `backend/src/utils/content_cleaner.py` to clean MDX content (remove Docusaurus syntax, comments, JSX, normalize Markdown).
- [X] T068 [US2] Create `backend/src/utils/mdx_chunker.py` to chunk text based on specified rules (300-600 tokens with overlap) and extract metadata (source path, chapter, section).
- [X] T069 [US2] Create `backend/src/services/embedding_service.py` to interface with Cohere API for embedding generation, including batch embedding calls.
- [X] T070 [US2] Create `backend/src/db/qdrant_client.py` to handle Qdrant client initialization and vector storage.
- [X] T071 [US2] Create `backend/src/db/postgres_client.py` to handle Neon Postgres client initialization and metadata storage.
- [X] T072 [US2] Define Postgres schema for chunk metadata in `backend/src/db/schema.sql`.
- [X] T073 [US2] Scaffold FastAPI project structure in `backend/`.
- [X] T074 [US2] Create `backend/src/api/ingest_router.py` with `POST /ingest` endpoint.
- [X] T075 [US2] Implement `Ingestion Service` logic in `backend/src/services/ingestion.py` to orchestrate cleaning, chunking, embedding, and storage.
- [X] T076 [US2] Develop a script (`backend/scripts/run_ingestion.py`) to trigger the `/ingest` endpoint and process all `docs/` content.
- [X] T077 [US2] Verify successful ingestion by checking Qdrant and Neon Postgres.

## Phase 1: Retrieval & Reasoning Backend

**Story Goal**: As a user of the Docusaurus robotics book, I want to ask questions about the book's content through a chat widget and receive accurate, relevant answers that are strictly derived from the book's information. (US1)
**Independent Test**: Can be fully tested by asking a question about a specific topic from the book and verifying the answer's accuracy and grounding in the text. (US1)

**Story Goal**: As a user, I want to select a specific passage of text within the Docusaurus book and ask the chatbot a question related to only that selected text to get focused information. (US3)
**Independent Test**: Can be tested by selecting a paragraph, querying the chatbot about it, and ensuring the response is based only on the selected text. (US3)

- [X] T078 [US1] Enhance `backend/src/db/qdrant_client.py` to perform vector search with payload filtering.
- [X] T079 [US1] Enhance `backend/src/db/postgres_client.py` to retrieve chunk metadata by ID.
- [X] T080 [US1] Create `backend/src/services/retrieval_service.py` to coordinate Qdrant search and Postgres retrieval.
- [X] T081 [US1] Create `backend/src/services/reasoning_service.py` to interface with Gemini API and develop prompt templates for Gemini, focusing on grounding and safety.
- [X] T082 [US1] Create `backend/src/api/query_router.py` with `POST /query` endpoint.
- [X] T083 [US1] Implement query logic using `retrieval_service` in `backend/src/api/query_router.py`.
- [X] T084 [US1] Create `backend/src/api/chat_router.py` with `POST /chat` endpoint.
- [X] T085 [US1] Implement chat logic combining `retrieval_service` and `reasoning_service` in `backend/src/api/chat_router.py`.
- [X] T086 [US3] Modify `backend/src/services/retrieval_service.py` to incorporate selected text for contextual filtering.

## Phase 2: Frontend Integration & Deployment

**Story Goal**: As a system operator, I want to check the health status of the RAG chatbot backend to ensure it is operational. (US4)
**Independent Test**: Can be tested by hitting the `/health` endpoint and expecting a successful response. (US4)

- [X] T087 [US4] Create `backend/src/api/health_router.py` with `GET /health` endpoint.
- [X] T088 [US4] Implement CORS middleware in `backend/src/main.py`.
- [X] T089 [US4] Implement API key authentication for backend endpoints.
- [X] T090 [US4] Implement basic rate-limiting in `backend/src/main.py`.
- [X] T091 Decided on ChatKit for frontend technology.
- [C] T092 If Streamlit, create `frontend/app.py` for the chat widget.
- [X] T093 Integrate ChatKit library into Docusaurus.
- [X] T093.1 [US1] Remove `frontend/chat_widget/index.html` and `frontend/chat_widget/client.js` as they are no longer needed.
- [X] T094 Modify Docusaurus theme (`docusaurus.config.js` or `src/theme/Layout.js`) to embed the frontend widget, ensuring adherence to the constitution's deployment policy (no alteration/removal of MCP-specific structures/metadata).
- [X] T095 Create `backend/Dockerfile` for FastAPI application.
- [X] T096 Create `render.yaml` (or similar) for Render deployment configuration.
- [ ] T097 If using a separate frontend, configure deployment for Vercel/Netlify.
- [X] T098 Conduct E2E testing of ingestion and chat flow.
- [ ] T099 Conduct UAT with target users.

## Cross-Cutting Concerns / Polish

- [X] T100 Implement comprehensive logging for ingestion, query, and chat events.
- [X] T101 Write comprehensive unit tests for core backend components, including `content_cleaner`, `mdx_chunker`, and `embedding_service`.
- [X] T102 Write comprehensive integration tests for the full RAG pipeline, covering ingestion, retrieval, and reasoning.
- [X] T103 Update `README.md` with setup and deployment instructions.
- [X] T104 Create `backend/.env.example` to document required environment variables: `GEMINI_API_KEY`, `COHERE_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `DATABASE_URL`.

## Task Dependencies

- Phase 0 tasks must be completed before Phase 1.
- Phase 1 tasks must be completed before Phase 2.
- Cross-Cutting Concerns can be addressed throughout development but are critical before final deployment.

## Parallel Execution Examples

- **Backend Development (Phase 0 & 1)**:
    - T067, T068, T069 (Content cleaning, chunking, embedding service) can be developed in parallel.
    - T070, T071, T072 (Qdrant, Postgres clients, schema) can be developed in parallel.
    - T073, T074, T075 (FastAPI scaffold, ingest endpoint, ingestion service) can be developed in parallel.
- **Frontend Development (Phase 2)**:
    - T091, T092, T093 (Frontend widget development) can be done while backend is being developed.

## Implementation Strategy

The implementation will follow an iterative approach, prioritizing core backend functionality (ingestion, retrieval, reasoning) before integrating the frontend and focusing on deployment. Each user story provides an independently testable increment.

**MVP Scope**: Phase 0 and Phase 1, combined with basic deployment of the backend, allowing content ingestion and API-based querying/chat.

