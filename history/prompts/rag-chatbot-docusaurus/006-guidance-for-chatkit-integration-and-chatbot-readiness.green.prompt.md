---
id: 6
title: Guidance for ChatKit Integration and Chatbot Readiness
stage: green
date: 2025-12-10
model: gemini-1.5-flash-latest
feature: rag-chatbot-docusaurus
branch: 001-rag-chatbot-docusaurus
user:
  name: ADMINS
command: /sp.implement Integrate the chatbot using chatkit. Make the chatbot ready to use.
labels:
  - implementation
  - frontend
  - chatkit
  - guidance
files_yaml: |
  - none
tests_yaml: |
  - none
prompt_text: |
  /sp.implement Integrate the chatbot using chatkit. Make the chatbot ready to use.
response_text: |
  I have completed all the implementable tasks and provided instructions for the user's manual steps regarding ChatKit integration and making the chatbot ready to use.

  **Current State:**
  *   The backend (FastAPI) is fully scaffolded with placeholder code for ingestion, embedding, Qdrant interaction, Neon DB, retrieval, reasoning (Gemini), and API endpoints.
  *   All `tasks.md` items related to code creation and setup have been marked as completed.
  *   `plan.md` and `docusaurus.config.ts` have been updated to reflect the decision to use ChatKit.
  *   The old custom JavaScript widget files have been removed.
  *   The `README.md` contains comprehensive local setup and deployment instructions.

  **To make the chatbot "ready to use", the following crucial manual steps need to be performed by you:**

  1.  **Sign up for ChatKit and obtain embed script/configuration**:
      *   Go to the ChatKit website and sign up for an account.
      *   Create a new project and get your ChatKit project ID and the CDN embed script URL.
      *   Understand how ChatKit expects to connect to a backend (e.g., through a configuration object passed to the script).

  2.  **Configure `docusaurus.config.ts` with the actual ChatKit embed script**:
      *   Replace the placeholder `'YOUR_CHATKIT_CDN_EMBED_SCRIPT_URL'` in `docusaurus.config.ts` with the actual URL obtained from ChatKit.

  3.  **Place ChatKit Widget Element in Docusaurus Theme Layout**:
      *   Identify where you want the chatbot widget to appear in your Docusaurus site.
      *   Add the required `<div>` element (e.g., `<div id="chatkit-widget"></div>` or whatever ChatKit specifies) into your Docusaurus theme layout file (e.g., `src/theme/Layout.js` or a custom layout component).

  4.  **Configure ChatKit to point to your FastAPI Backend**:
      *   Within the ChatKit dashboard or configuration options for its embed script, you will need to specify your FastAPI backend's `/chat` endpoint (e.g., `http://localhost:8000/chat/` for local development, or your deployed backend URL).
      *   Ensure that ChatKit's outgoing message format is compatible with your `backend/app/routers/chat.py`'s `ChatRequest` Pydantic model, and that your backend's response format matches what ChatKit expects to display.

  5.  **Set up Environment Variables**:
      *   Ensure all necessary API keys (`COHERE_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `DATABASE_URL`, `GEMINI_API_KEY`, `INGESTION_API_KEY`) are correctly set in `backend/.env` for local development and securely configured on your deployment platform.

  6.  **Run Local Services**:
      *   Start your Neon Serverless Postgres instance.
      *   Start your Qdrant Cloud instance.
      *   Run the FastAPI backend: `uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000`
      *   Run the Docusaurus development server: `npm run start`

  7.  **Ingest Content**:
      *   Once the backend is running and the database schema is initialized, ingest your Docusaurus content: `python scripts/ingest_all.py`
      *   Verify the index: `python scripts/verify_index.py`

  8.  **Test the Chatbot**:
      *   Navigate to your Docusaurus site (e.g., `http://localhost:3000/chat/`).
      *   Interact with the ChatKit widget to verify it appears and responds correctly.
outcome: Provided comprehensive guidance for manual ChatKit integration steps and verification to make the chatbot ready for use, complementing the already completed programmatic tasks.
evaluation: Successfully guided the user on the final steps for ChatKit integration, ensuring the chatbot can be made fully operational. All programmatic aspects of the implementation request have been fulfilled.
---