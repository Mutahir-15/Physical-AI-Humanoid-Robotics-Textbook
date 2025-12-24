# Implementation Plan: Free-Tier RAG Chatbot Integration for the Robotics Book

**Branch**: `001-robotics-course-spec` | **Date**: 2025-12-07 | **Spec**: `specs/001-robotics-course-spec/spec.md`
**Input**: Feature specification from `specs/001-robotics-course-spec/spec.md` (RAG Chatbot Future Integration Notes)

## Summary

This plan details the end-to-end strategy for integrating a free-tier Retrieval-Augmented Generation (RAG) chatbot into the existing Docusaurus-based "Physical AI & Humanoid Robotics Course" book. The system will leverage Gemini API for LLM responses, Cohere for free embeddings, Qdrant Cloud (free tier) for vector storage, FastAPI for the backend API, OpenAI Agents SDK for local orchestration, and a Streamlit frontend embedded within the Docusaurus site. The plan ensures no paid services are required for its core functionality.

## Technical Context

**Language/Version**: Python 3.x (for Chunking Service, FastAPI, OpenAI Agents, Streamlit), JavaScript/TypeScript (for Docusaurus integration).
**Primary Dependencies**:
*   **LLM**: Google Gemini API (free tier)
*   **Embeddings**: Cohere Embed v3 (free tier)
*   **Vector Store**: Qdrant Cloud (free tier)
*   **Backend**: FastAPI
*   **Agent Orchestration**: OpenAI Agents SDK (local runtime only)
*   **Frontend**: Streamlit, Docusaurus (for embedding)
*   **Other Tools**: `langchain` (for text splitting, if used), `qdrant-client`, `cohere-sdk`, `uvicorn`.
**Storage**:
*   Document Source: Docusaurus `/docs/*.mdx` content (exported to raw text).
*   Vector Store: Qdrant Cloud free-tier collection.
*   Metadata Store: (Optional, but planned for future enhancement) Neon Postgres free-tier for comprehensive chunk data storage.
**Testing**: Unit tests for chunking, embedding, retrieval, and RAG logic; integration tests for API endpoints; end-to-end testing of chatbot functionality in Streamlit UI; manual verification of grounded responses.
**Target Platform**: Web (Streamlit embedded in Docusaurus). Backend deployable to free-tier cloud platforms (Render, Deta Space, Railway).
**Project Type**: RAG Chatbot as an interactive educational tool.
**Performance Goals**: Sub-5 second response time for typical queries; efficient embedding generation; robust handling of rate limits.
**Constraints**: Strictly adhere to free-tier limits of all chosen services; local-only use of OpenAI Agents SDK; seamless embedding into Docusaurus via iframe.
**Scale/Scope**: Single RAG chatbot for the existing book content, handling conversational queries.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The plan aligns with all guiding principles of the project constitution:
*   **Principle 1: Technical Accuracy and Rigor**: The RAG system aims for accurate information retrieval and grounded responses, maintaining technical fidelity to the book's content.
*   **Principle 2: Practical, Simulation-First Learning**: While the chatbot itself is not a simulation, it enhances the practical learning experience by providing immediate answers based on the book's practical content.
*   **Principle 3: Clear and Consistent Content**: The chatbot's responses will be derived from the book's content, which adheres to this principle, ensuring clarity and consistency in its answers.
*   **Principle 4: Modular and Structured Design**: The RAG system is designed with modular components (chunking, embedding, vector store, backend, LLM, agent, frontend) that integrate into the existing Docusaurus structure. Deployment via GitHub Pages is the existing book deployment, and the chatbot will integrate into it.
*   **Principle 5: Capstone-Driven Progression**: The chatbot serves as an advanced learning aid, reinforcing the knowledge gained through the modules and potentially helping learners with their Capstone Project.

## Project Structure

### Architecture Sketch

*   **High-level RAG system architecture**:
    *   **Offline Data Ingestion**: Docusaurus MDX files -> Chunking Service (Python) -> Cohere Embeddings -> Qdrant (vectors + metadata).
    *   **Online Query Flow**: Streamlit Frontend (user query) -> FastAPI Backend (Retrieval API) -> Qdrant (vector search) -> OpenAI Agents SDK (orchestration) -> Gemini API (LLM response) -> Streamlit Frontend.
*   **Component Interactions**:
    *   **Frontend (Streamlit)**: Embedded via `iframe` in Docusaurus. Communicates with FastAPI backend.
    *   **FastAPI Backend**: Exposes `/query` and other endpoints. Acts as the central hub, orchestrating calls to Qdrant, OpenAI Agents, and Gemini.
    *   **Qdrant**: Stores vector embeddings and metadata of book chunks.
    *   **Cohere**: Used *offline* for generating embeddings during the ingestion phase.
    *   **Gemini API**: Provides the core LLM reasoning based on retrieved context.
    *   **OpenAI Agents SDK**: Runs *locally within the FastAPI process* to orchestrate tools (like retrieval) and manage conversational memory.
*   **Where code and configuration files will live**:
    *   `/rag/ingestion/`: Chunking and embedding pipeline scripts.
    *   `/rag/backend/`: FastAPI application code.
    *   `/rag/frontend/`: Streamlit application code.
    *   `/rag/docs/`: Documentation specific to the RAG system.
    *   `/rag/configs/`: Configuration files (e.g., Qdrant collection config, prompt templates).

### Section & Module Structure

*   **Ingestion Pipeline (`/rag/ingestion/`)**: Scripts for `chunking`, `embedding`, and `indexing`.
*   **Backend (`/rag/backend/`)**: FastAPI application, including `retrieval_api.py`, `llm_service.py`, `agent_orchestrator.py`.
*   **Frontend (`/rag/frontend/`)**: Streamlit app (`app.py`).
*   **Docusaurus Integration**: A new Docusaurus page `/chat/index.mdx` will embed the Streamlit app.

## Production Workflow

*   **Step-by-step development workflow**:
    1.  Develop and test chunking pipeline.
    2.  Develop and test embedding generation and Qdrant indexing.
    3.  Develop FastAPI retrieval API endpoints.
    4.  Implement RAG chain with Gemini and integrate OpenAI Agents.
    5.  Develop Streamlit frontend.
    6.  Integrate Streamlit into Docusaurus.
    7.  Deploy backend and frontend components.
*   **Continuous integration for new content**: When book content updates, the chunking and embedding pipeline must be re-run to update Qdrant.
*   **API key management**: All API keys (Gemini, Cohere, Qdrant) will be stored securely as environment variables in the deployment environment.

## Decisions Needing Documentation (ADR)

*   **Architectural Decision: RAG Architecture Choice (Generative vs. Conversational)**
    *   **Options Considered**: Pure generative LLM, simple retrieval (context stuffing), RAG with agentic orchestration.
    *   **Decision**: RAG with local OpenAI Agent orchestration.
    *   **Rationale**: Offers a robust, grounded approach to answers while providing flexibility for tool use (retrieval, citation) and conversational memory, all within free-tier constraints.
    *   **Tradeoffs**: Adds complexity compared to simple RAG, requires careful agent prompting.
*   **Architectural Decision: Frontend Embedding in Docusaurus**
    *   **Options Considered**: Docusaurus native React components, external Streamlit app via iframe.
    *   **Decision**: External Streamlit app embedded via iframe.
    *   **Rationale**: Leverages Streamlit's rapid UI development for chat interfaces, keeping the RAG application separate from Docusaurus build process. Avoids complex Docusaurus plugin development.
    *   **Tradeoffs**: Potential iframe sizing/styling issues, possible SEO limitations for the chatbot itself.
*   **Architectural Decision: LLM and Embedding Model Selection**
    *   **Options Considered**: Various free-tier LLMs and embedding models.
    *   **Decision**: Gemini API for LLM, Cohere Embed v3 for embeddings.
    *   **Rationale**: Both offer generous free tiers and are industry-leading, providing high-quality results for RAG tasks. Gemini's multi-modality is a bonus for potential future enhancements.
    *   **Tradeoffs**: Dependence on specific vendor APIs, potential for future changes in free-tier offerings.

## Quality Validation Strategy

*   **Unit Tests**: For each component (chunking, embedding, FastAPI endpoints, agent tools).
*   **Integration Tests**: Verifying communication between FastAPI and Qdrant, FastAPI and Gemini/OpenAI Agents.
*   **End-to-End Tests**: Automated tests simulating user queries through Streamlit to verify correct RAG responses and source citation.
*   **Manual Verification**: Human evaluation of chatbot responses for accuracy, relevance, and adherence to contextual boundaries.
*   **Performance Testing**: Monitoring response times and resource usage on free-tier deployments.

## Technical Execution Details

*   **Chunking Pipeline**:
    *   Script to load `/docs/**/*.mdx` content.
    *   Robust Markdown stripping and cleaning.
    *   RecursiveCharacterTextSplitter for fixed-size segments (300–600 tokens) with 50–100 tokens overlap.
    *   Export chunks with metadata (source_path, chapter, section, token_count) to `chunks.json` for intermediate storage.
*   **Embeddings Pipeline**:
    *   Python script to read `chunks.json`.
    *   Call Cohere Embed v3 API. Implement batching and rate limiting strategies (e.g., `time.sleep()`) to stay within free-tier limits.
    *   Store embeddings with metadata in Qdrant Cloud. Verify indexing and correct metadata mapping.
*   **Retrieval Layer (FastAPI)**:
    *   Endpoints: `/query` (main chat endpoint), `/health` (status check), `/retrieve` (raw chunk retrieval for debugging/testing).
    *   Qdrant similarity search: Use Cosine distance, `top_k` results.
    *   Boundary logic: Implement `max_results` (e.g., 3-5 chunks), and filtering by `chapter` or `section` metadata using Qdrant's payload filtering.
*   **RAG Reasoning Layer**:
    *   RAG chain implementation: User query -> Retrieval from Qdrant -> Assemble context -> Gemini API call with grounded prompt.
    *   Prompt templates: Design robust templates for answer generation, ensuring citation-aware responses and explicit refusal for out-of-scope questions.
*   **Agent Integration (OpenAI Agents SDK)**:
    *   Run agents SDK in local mode within the FastAPI application.
    *   Register tools: `retrieve_context(query, filters)`, `format_answer(context, question)`, `cite_sources(retrieved_metadata)`.
    *   Implement memory management (e.g., `agent.add_memory(cap=false)`).
    *   Design tool-calling structure and agent prompts for effective orchestration.
*   **Frontend (Streamlit)**:
    *   Basic chat interface: text input for user query, display area for chatbot response.
    *   Render source snippets (chapter/section) alongside the answer.
    *   Markdown answer rendering.
    *   Custom styling with `Streamlit` or `ChatKit` if needed.
*   **Docusaurus Integration**:
    *   Create `docs/chat/index.mdx` page.
    *   Embed Streamlit app URL using an `iframe` tag within the MDX.
    *   Address potential `iframe` sizing and responsiveness issues with custom CSS in Docusaurus.

## Phase-Based Plan

### Phase A: Chunking Pipeline (Duration: 1 week)

*   **Objective**: Create a robust system for converting MDX book content into clean, chunked text with rich metadata.
*   **Tasks**:
    *   Develop script (`/rag/ingestion/chunk_processor.py`) to load all `/docs/**/*.mdx`.
    *   Implement Markdown stripping and cleaning logic.
    *   Integrate `RecursiveCharacterTextSplitter` (or equivalent) for chunking (300-600 tokens, 50-100 overlap).
    *   Develop metadata extraction from file paths and content.
    *   Generate `chunks.json` output with chunk text and metadata.
    *   Unit tests for cleaning, chunking, and metadata extraction.

### Phase B: Embeddings Pipeline (Duration: 1.5 weeks)

*   **Objective**: Generate high-quality embeddings for all chunks and index them efficiently in Qdrant Cloud.
*   **Tasks**:
    *   Develop script (`/rag/ingestion/embed_indexer.py`) to read `chunks.json`.
    *   Integrate Cohere Embed v3 API calls (batching, rate limits).
    *   Initialize and configure Qdrant Cloud collection (free tier).
    *   Push vectors and payload (metadata) to Qdrant.
    *   Verify indexing correctness and searchability.
    *   Unit and integration tests for embedding generation and Qdrant interaction.

### Phase C: Retrieval Layer (Duration: 2 weeks)

*   **Objective**: Build a FastAPI backend service capable of receiving queries and retrieving relevant information from Qdrant.
*   **Tasks**:
    *   Setup FastAPI project (`/rag/backend/`).
    *   Implement `/query`, `/health`, `/retrieve` endpoints.
    *   Integrate Qdrant client for vector similarity search (cosine distance).
    *   Implement `max_results` and metadata filtering logic (chapter/section).
    *   Implement an optional re-ranking step for retrieved chunks.
    *   Unit and integration tests for all API endpoints.

### Phase D: RAG Reasoning Layer (Duration: 2.5 weeks)

*   **Objective**: Integrate Gemini API with the retrieval layer to generate grounded, conversational responses.
*   **Tasks**:
    *   Develop core RAG chain logic using FastAPI endpoints and Gemini API.
    *   Design robust prompt templates for Gemini, ensuring context grounding, citation-awareness, and refusal for out-of-scope questions.
    *   Develop error handling for LLM calls and context assembly.
    *   Test RAG chain with various queries (in-scope, out-of-scope, ambiguous).

### Phase E: Agent Integration (Duration: 2 weeks)

*   **Objective**: Orchestrate the RAG process using OpenAI Agents SDK for advanced conversational capabilities and tool use.
*   **Tasks**:
    *   Integrate OpenAI Agents SDK locally within FastAPI.
    *   Define and register agent tools: `retrieve_context`, `format_answer`, `cite_sources`.
    *   Implement agent memory management.
    *   Design agent prompts for effective tool orchestration and conversational flow.
    *   Test agent's ability to use tools, manage conversation, and provide grounded answers.

### Phase F: Frontend (Streamlit) (Duration: 1.5 weeks)

*   **Objective**: Create an interactive chat interface and seamlessly embed it into the Docusaurus book.
*   **Tasks**:
    *   Develop Streamlit application (`/rag/frontend/app.py`) for the chat UI.
    *   Implement user input, response display, and source citation rendering.
    *   Integrate with FastAPI `/query` endpoint.
    *   Create Docusaurus page `docs/chat/index.mdx` to embed the Streamlit app via iframe.
    *   Address `iframe` styling, sizing, and responsiveness in Docusaurus CSS.
    *   End-to-end testing of the frontend.

## Deployment Strategy

### Book

*   Already deployed via Vercel. The chatbot will integrate into this existing deployment.

### FastAPI Backend

*   **Platform**: Deploy to free-tier provider like Render, Deta Space, or Railway (user's choice).
*   **Configuration**: Store sensitive API keys (GEMINI_API_KEY, COHERE_API_KEY, QDRANT_API_KEY, QDRANT_URL) as environment variables in the chosen deployment platform.
*   **Monitoring**: Implement basic health checks (`/health` endpoint) for deployment.

### Streamlit Frontend

*   **Platform**: Deploy on Streamlit Cloud (free tier).
*   **Configuration**: Configure Streamlit app to point to the deployed FastAPI backend URL.

### Integration

*   **Docusaurus Chatbot Page**: Create a dedicated Docusaurus page at `/chat/index.mdx` which embeds the deployed Streamlit application using an `iframe`.

## Risks & Mitigation

*   **Cohere Free Tier Rate Limits**:
    *   **Mitigation**: Implement exponential backoff and retry logic in the embedding pipeline. Batch processing of chunks. Add `time.sleep()` between API calls.
*   **Qdrant Collection Limits (Free Tier)**:
    *   **Mitigation**: Optimize metadata storage to be compact. Ensure only necessary payload fields are stored. If limits are reached, explore options for alternative free-tier vector DBs or local Qdrant instance.
*   **Streamlit iFrame Sizing/Styling in Docusaurus**:
    *   **Mitigation**: Utilize custom CSS within Docusaurus to control `iframe` dimensions and responsive behavior. Test across various screen sizes.
*   **FastAPI Cold Starts on Free Tiers**:
    *   **Mitigation**: Implement a small, scheduled "keep-alive" job (e.g., a simple ping to `/health`) to prevent the free-tier service from spinning down due to inactivity.
*   **OpenAI Agents SDK Local Runtime Compatibility/Performance**:
    *   **Mitigation**: Thorough testing of the agent's performance and stability within the FastAPI environment. Monitor resource usage.

## Deliverables

✓ Chunking pipeline documentation (`/rag/docs/chunking_strategy.mdx`) and script (`/rag/ingestion/chunk_processor.py`).
✓ Embeddings pipeline documentation (`/rag/docs/indexing_pipeline.mdx`) and script (`/rag/ingestion/embed_indexer.py`).
✓ Vector DB indexing in Qdrant (populated collection).
✓ Retrieval API (FastAPI backend with `/query`, `/retrieve`, `/health` endpoints).
✓ Gemini-based RAG chain with prompt templates.
✓ OpenAI Agent orchestration (`/rag/backend/agent_orchestrator.py`).
✓ Frontend UI (Streamlit app, `/rag/frontend/app.py`).
✓ Deployment setup and configuration for FastAPI and Streamlit.
✓ Documentation for all components within `/rag/docs/`.

End of Plan.