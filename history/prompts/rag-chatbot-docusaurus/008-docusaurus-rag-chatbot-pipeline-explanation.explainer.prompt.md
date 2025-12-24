---
id: 008
title: Docusaurus RAG Chatbot Pipeline Explanation
stage: explainer
date: 2025-12-17
surface: agent
model: gemini-1.5-flash-latest
feature: rag-chatbot-docusaurus
branch: 001-rag-chatbot-docusaurus
user: user
command: /sp.clarify Explain the RAG mental model again, but this time: 1. Use THIS project only (Docusaurus book → RAG chatbot) 2. Explain it as a pipeline from: - User question - To final answer on UI 3. Explain what happens when: - User asks a general question - User selects specific text and asks a question 4. Clearly explain: - What goes into Qdrant - What goes into Postgres - What NEVER goes to the LLM 5. Explain common beginner mistakes in RAG and how this design avoids them No code. No file changes. Pure explanation. End with: READY FOR REBUILD SEQUENCE.
labels: [rag, chatbot, pipeline, explanation, mental-model, docusaurus]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:

tests:

---

## Prompt

Context for prioritization: I want to lock my understanding before rebuilding. Explain the RAG mental model again, but this time: 1. Use THIS project only (Docusaurus book → RAG chatbot) 2. Explain it as a pipeline from: - User question - To final answer on UI 3. Explain what happens when: - User asks a general question - User selects specific text and asks a question 4. Clearly explain: - What goes into Qdrant - What goes into Postgres - What NEVER goes to the LLM 5. Explain common beginner mistakes in RAG and how this design avoids them No code. No file changes. Pure explanation. End with: READY FOR REBUILD SEQUENCE.

## Response snapshot

Provided a detailed explanation of the Docusaurus RAG Chatbot pipeline, covering user interaction scenarios, data storage in Qdrant and Postgres, what stays out of the LLM, and common RAG beginner mistakes and their avoidance in this design.

## Outcome

- ✅ Impact: Provided a detailed explanation of the Docusaurus RAG Chatbot pipeline and best practices for the user's understanding before rebuilding.
- 🧪 Tests: N/A - Explanation task, no tests.
- 📁 Files: N/A - No files modified.
- 🔁 Next prompts: READY FOR REBUILD SEQUENCE.
- 🧠 Reflection: Successfully provided a comprehensive explanation of the RAG pipeline as requested, addressing specific project details and common pitfalls to aid the user's rebuild process.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
