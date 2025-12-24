---
id: 21
title: Plan Free-Tier RAG Chatbot Integration
stage: plan
date: 2025-12-07
surface: agent
model: Gemini
feature: 001-robotics-course-spec
branch: 001-robotics-course-spec
user: user
command: /sp.plan Plan: Free-Tier RAG Chatbot Integration for the Robotics Book
labels: ["rag", "chatbot", "plan", "free-tier"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- specs/001-robotics-course-spec/plan.md
tests:
- N/A
---

## Prompt

```text
---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
---

## User Input

```text
Plan: Free-Tier RAG Chatbot Integration for the Robotics Book

Objective:
Design a fully free, end-to-end Retrieval-Augmented Generation (RAG) chatbot system integrated into the Docusaurus book, using:
• Gemini API for LLM responses  
• Cohere free embeddings  
• Qdrant Cloud (free tier) for vector search  
• FastAPI backend for chat/inference  
• OpenAI Agents SDK (free local runtime)  
• Streamlit frontend embedded inside the book  
No paid services required.

------------------------------------------------------------
1. System Architecture
------------------------------------------------------------
1.1 Components
- Document Source: Docusaurus /docs/*.mdx exported to raw text
- Chunking Service: local Python service
- Embedding Service: Cohere free-tier API
- Vector Store: Qdrant Cloud free-tier collection
- Metadata Store: (Optional) Neon Postgres free-tier
- Retrieval API: FastAPI backend
- LLM Reasoning Engine: Gemini API
- Agent Orchestration: OpenAI Agents SDK (free local runtime)
- Frontend UI: Streamlit (embedded inside the Docusaurus site via iframe)

1.2 Data Flow
1. Export docs → text chunks  
2. Generate embeddings via Cohere  
3. Store vectors + metadata in Qdrant  
4. User submits query in Streamlit  
5. FastAPI receives query → retrieves relevant chunks  
6. OpenAI-Agent orchestrates  
7. Gemini generates grounded answer  
8. Send response back to UI

------------------------------------------------------------
2. Free-Tier Technology Strategy
------------------------------------------------------------
2.1 LLM:
- Gemini API key (free tier)

2.2 Embeddings:
- Cohere Embed v3 (free tier)
- Batch or streaming mode to avoid rate limits

2.3 Vector DB:
- Qdrant Cloud free-tier
  • 1 collection  
  • Enough for the book content  

2.4 Backend:
- FastAPI (Free)
- Host locally or deploy to:  
  • Render free tier  
  • Deta Space  
  • Railway free plan (optional)

2.5 Agent Runtime:
- OpenAI Agents SDK (free local mode only)
- No paid OpenAI usage

2.6 Frontend:
- Streamlit (free)
- Embedded in Docusaurus via iframe  
- Optionally: ChatKit for UI styling

------------------------------------------------------------
3. Implementation Strategy
------------------------------------------------------------

3.1 Phase A — Chunking Pipeline
- Script to load /docs/**/*.mdx
- Strip markdown & clean
- Chunk into fixed-size segments (300–600 tokens)
- Overlap 50–100 tokens
- Export chunks.json + metadata

3.2 Phase B — Embeddings Pipeline
- Send chunks to Cohere embeddings API
- Store results locally first
- Push to Qdrant Cloud via REST/Python client
- Verify indexing + metadata

3.3 Phase C — Retrieval Layer
- FastAPI endpoints:
  • /query
  • /health
  • /retrieve
  • /rerank (optional)
- Qdrant similarity search
- Boundary logic:
  • max_results  
  • chapter filter  
  • section filter  

3.4 Phase D — RAG Reasoning Layer
- Implement RAG chain:
  • Query → retrieve → assemble context → Gemini response
- Add prompt templates:
  • answer generation  
  • citation-aware responses  
  • refusal for out-of-scope questions  

3.5 Phase E — Agent Integration
- Use OpenAI Agents SDK locally:
  • agent.register_tool(retrieve_tool)
  • agent.add_memory(cap=false)
- Deploy agent router on FastAPI
- Add tool-calling structure:
  • retrieve_context  
  • format_answer  
  • cite_sources  

3.6 Phase F — Frontend (Streamlit)
- Simple chat interface:
  • user query  
  • source snippets  
  • markdown answer  
- Insert into Docusaurus:
  • via iframe  
  • custom page under /chat  

------------------------------------------------------------
4. Deployment Strategy
------------------------------------------------------------
4.1 Book
- Already deployed (GitHub Pages)

4.2 FastAPI Backend
- Deploy to Render/Deta/Railway free plan
- Store secrets in environment variables:
  • GEMINI_API_KEY  
  • COHERE_API_KEY  
  • QDRANT_API_KEY  
  • QDRANT_URL  

4.3 Streamlit
- Deploy on Streamlit Cloud (free)

4.4 Integration
- Add a Chatbot page in Docusaurus:
  • /chat/index.mdx  
  • Embed iframe to Streamlit URL

------------------------------------------------------------
5. Risks & Mitigation
------------------------------------------------------------
- Cohere free rate limits → add sleep & batch processing  
- Qdrant collection limits → compress metadata  
- Streamlit iframe sizing → custom CSS  
- FastAPI cold starts → small KeepAlive job  

------------------------------------------------------------
6. Deliverables
------------------------------------------------------------
✓ chunking pipeline  
✓ embeddings pipeline  
✓ vector DB indexing  
✓ retrieval API  
✓ gemini-based RAG chain  
✓ OpenAI Agent orchestration  
✓ frontend UI  
✓ deployment setup  
✓ documentation inside /rag/docs/*

End of Plan.
```

## Response snapshot

I have successfully written the complete implementation plan to `specs/001-robotics-course-spec/plan.md`. This plan covers all the details provided in the user's prompt, organized into the `plan-template.md` structure.

**Reporting:**
*   **Branch**: `001-robotics-course-spec`
*   **IMPL_PLAN Path**: `specs/001-robotics-course-spec/plan.md`
*   **Generated Artifacts**:
    *   Updated `specs/001-robotics-course-spec/plan.md`

## Outcome

- ✅ Impact: Successfully generated a detailed implementation plan for the RAG chatbot.
- 🧪 Tests: N/A
- 📁 Files: Updated 1 file (`specs/001-robotics-course-spec/plan.md`).
- 🔁 Next prompts: User will likely proceed with generating tasks based on this plan.
- 🧠 Reflection: Successfully integrated a complex user-provided plan into the template, addressing all required sections.

## Evaluation notes (flywheel)

- Failure modes observed: `create-phr.sh` script failed due to PowerShell environment, necessitating manual PHR creation.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
