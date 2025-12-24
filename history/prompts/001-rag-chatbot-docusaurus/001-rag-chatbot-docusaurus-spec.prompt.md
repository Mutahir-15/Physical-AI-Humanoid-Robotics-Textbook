---
id: 001
title: RAG Chatbot Docusaurus Spec
stage: spec
date: 2025-12-10
surface: agent
model: (unknown)
feature: 001-rag-chatbot-docusaurus
branch: 001-rag-chatbot-docusaurus
user: (unknown)
command: /sp.specify
labels: ["rag-chatbot", "docusaurus", "specification"]
links:
  spec: specs/001-rag-chatbot-docusaurus/spec.md
  ticket: null
  adr: null
  pr: null
files:
- specs/001-rag-chatbot-docusaurus/spec.md
- specs/001-rag-chatbot-docusaurus/checklists/requirements.md
tests:
null
---

## Prompt

Title: RAG Chatbot Integration for Docusaurus Book (Free Stack) Objective: Build a Retrieval-Augmented Generation (RAG) chatbot for the live Docusaurus robotics book using FREE-tier services: Gemini API (LLM), Cohere Embed v3 (embeddings), Qdrant Cloud (vectors), Neon Serverless Postgres (metadata), FastAPI backend, and ChatKit or lightweight Streamlit UI embedded into the book. Functional Requirements (high level): - Ingest docs/ MDX -> clean text -> chunking (300-600 tokens) and overlap - Create embeddings with Cohere; store vectors in Qdrant - Store metadata (source file, chapter, chunk_id, start_pos) in Neon Postgres - Expose REST endpoints: POST /ingest, POST /query, POST /chat, GET /health - Provide "selected-text only" query mode - Use Gemini API for reasoning/answer generation, strictly grounded in retrieved context - Frontend widget (ChatKit or Streamlit iframe) embedded across all pages - Security: API-key for backend, CORS restricted to book domain, basic rate-limiting Non-Functional Requirements: - All services must operate in free-tier limits - Typical response latency under ~2s (after retrieval) - Modular code (services/, routers/, db/, utils/) - Environment variables only for secrets - Logging of ingest/query/chat - Tests: basic unit and integration Acceptance Criteria: - At least 98% of book content ingested and indexed - Chat widget visible on every page - User-selected-text → accurate answer flow works - Backend reachable and stable on free-tier host - Answering is grounded to retrieved content (no hallucinations) Constraints: - Must use Cohere for embeddings, Qdrant for vectors, Neon for metadata, Gemini for LLM - No paid services required to prototype & demo - Integrate into current Docusaurus deployment Deliverable summary: - Spec doc + plan + executable tasks - Ingestion scripts, embedding pipeline, Qdrant index, Neon schema - FastAPI backend with endpoints - Chat widget UI integrated into Docusaurus - Deployment scripts and docs End.

## Response snapshot

Successfully created the feature specification, checklist, and validated the specification. All checks have passed. Ready for /sp.plan.

## Outcome

- ✅ Impact: Created a detailed feature specification for the RAG chatbot integration, including user stories, functional requirements, and success criteria.
- 🧪 Tests: No automated tests were run at this stage; specification validation was manual against a checklist.
- 📁 Files: Created `spec.md` and `checklists/requirements.md` for the new feature.
- 🔁 Next prompts: The next expected prompt is `/sp.plan` to begin planning based on the specification.
- 🧠 Reflection: The `create-new-feature.ps1` script failed to parse due to complex arguments, requiring manual steps. The `create-phr.sh` script also failed due to environment constraints, requiring manual PHR creation.

## Evaluation notes (flywheel)

- Failure modes observed: Script parsing error, environment-specific script execution failure.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
