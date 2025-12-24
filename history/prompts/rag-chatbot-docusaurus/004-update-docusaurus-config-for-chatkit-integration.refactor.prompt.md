---
id: 4
title: Update Docusaurus Config for ChatKit Integration
stage: refactor
date: 2025-12-10
model: gemini-1.5-flash-latest
feature: rag-chatbot-docusaurus
branch: 001-rag-chatbot-docusaurus
user:
  name: ADMINS
command: /sp.implement We have to build the UI of the chatbot using chatkit. What should we do now?
labels:
  - refactor
  - frontend
  - chatkit
files_yaml: |
  - specs/001-rag-chatbot-docusaurus/plan.md
  - specs/001-rag-chatbot-docusaurus/tasks.md
  - docusaurus.config.ts
tests_yaml: |
  - none
prompt_text: |
  We have to build the UI of the chatbot using chatkit. What should we do now?
response_text: |
  I have updated the `plan.md` and `tasks.md` to reflect the decision to use ChatKit. I also updated `docusaurus.config.ts` with a placeholder for the ChatKit embed script.

  **Summary of actions:**
  *   Updated `plan.md` to reflect ChatKit as the chosen frontend technology in the Summary, Technical Context, High-Level Architecture, Phase 2 Milestones, Component Responsibilities, and Deployment Targets sections.
  *   Updated `tasks.md`:
      *   Marked T091 as completed and updated its description to reflect the ChatKit decision.
      *   Marked T092 (Streamlit) as cancelled.
      *   Updated T093's description to reflect ChatKit integration.
      *   Added a new task T093.1 to remove the custom JS widget files (`frontend/chat_widget/index.html` and `frontend/chat_widget/client.js`).
  *   Updated `docusaurus.config.ts` with a placeholder for the ChatKit embed script.

  **Next Steps for you:**

  1.  **Retrieve ChatKit Embed Script**: Get the actual CDN embed script URL from your ChatKit account.
  2.  **Modify `docusaurus.config.ts`**: Replace `'YOUR_CHATKIT_CDN_EMBED_SCRIPT_URL'` with the actual URL.
  3.  **Place ChatKit Widget Element**: Add the required `<div>` for the ChatKit widget in your Docusaurus theme layout (e.g., `src/theme/Layout.js` or `src/components/MyLayout.js` if you have a custom layout).
  4.  **Configure ChatKit to point to your FastAPI Backend**: Set up the connection between the ChatKit frontend and your `http://localhost:8000/chat/` (or deployed) endpoint.
  5.  **Test**: Start your Docusaurus development server (`npm run start`) and your FastAPI backend (`uvicorn backend.app.main:app --reload`). Test the chatbot functionality.
  6.  **Mark T093.1 as complete (remove files)**: Once ChatKit is integrated, you can delete `frontend/chat_widget/index.html` and `frontend/chat_widget/client.js`.
outcome: Updated plan.md, tasks.md, and docusaurus.config.ts to reflect the new decision to use ChatKit for the frontend UI. Provided instructions for ChatKit integration.
evaluation: Successfully adapted the project plan and configuration to the new user requirement for ChatKit. Identified and updated all relevant artifacts and provided clear next steps.
---