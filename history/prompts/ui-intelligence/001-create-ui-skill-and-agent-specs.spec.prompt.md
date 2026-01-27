---
id: "001"
title: "Create UI Skill and Agent Specs"
stage: "spec"
date: "2026-01-27"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "ui-intelligence"
branch: "main"
user: "user"
command: "write_file"
labels: ["ui", "spec", "skills", "agent"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/skills-and-agents/ui-skill.md"
  - ".specify/skills-and-agents/ui-agent.md"
tests: []
---

## Prompt
Perfect! Now, You are a senior Product Engineer and UX Architect working on a spec-driven AI system.

Context:
- This is a documentation-first AI chatbot project.
- Backend: FastAPI + vector search (Qdrant) + RAG.
- Frontend: Docusaurus (NOT Next.js).
- The current UI is functional but visually basic.
- Goal: Make the UI feel "extraordinary" using reusable intelligence, not heavy visuals.

Your task:
1. Design a reusable UI intelligence layer using spec-kit plus.
2. Write TWO files:
   - ui-skill.md
   - ui-agent.md

Constraints:
- Do NOT introduce Flowise, Docker, or external UI frameworks.
- UI must remain lightweight and documentation-focused.
- Design must enhance clarity, hierarchy, and intelligence—not animation gimmicks.
- The UI should feel “smart”, adaptive, and purposeful.

Focus areas:
- Intelligent content highlighting
- Context-aware chat responses
- Progressive disclosure of information
- Query-aware UI feedback
- Smart empty states
- Confidence signaling (why an answer was returned)
- Reusable UI reasoning patterns

--------------------------------------------------
FILE 1: ui-skill.md
--------------------------------------------------

Define reusable UI SKILLS that can be invoked across the app.

Each skill must include:
- Skill Name
- Intent
- Trigger Condition
- Input Signals
- UI Behavior
- Reusability Scope
- Failure / Fallback Behavior

Required skills (you may add more):
- ContextAwareAnswerDisplay
- SourceGroundingHighlighter
- AnswerConfidenceIndicator
- QueryIntentClassifier (UI-level, not ML)
- ProgressiveAnswerReveal
- EmptyStateIntelligence
- RetrievalTraceViewer (for judges)
- SelectedTextContextMode
- ExplanationFirstMode (why before what)

--------------------------------------------------
FILE 2: ui-agent.md
--------------------------------------------------

Define a UI AGENT that orchestrates the skills.

Include:
- Agent Name
- Responsibilities
- Decision Flow (step-by-step)
- Skill Invocation Order
- User Interaction States
- Error Recovery Strategy
- Deterministic vs Adaptive Behavior
- How the agent improves UX without adding visual noise

The UI Agent should:
- Decide HOW answers are shown, not WHAT the answer is
- Make the UI feel responsive to user intent
- Adapt layout and emphasis based on query type
- Support judges understanding system behavior

--------------------------------------------------
Tone & Output Rules:
- Write clean, structured markdown
- No code unless absolutely necessary
- Use precise language (spec-driven style)
- Think like a hackathon judge reading this
- The output should be immediately usable in a real project

Start now and output ONLY the two markdown files.

## Response
Created `ui-skill.md` and `ui-agent.md` in `.specify/skills-and-agents`. These files define the reusable UI skills (such as `ContextAwareAnswerDisplay`, `SourceGroundingHighlighter`, `AnswerConfidenceIndicator`, etc.) and the `InterfaceOrchestrator` agent logic to manage the user experience intelligently within the Docusaurus environment, without adding heavy frameworks.
