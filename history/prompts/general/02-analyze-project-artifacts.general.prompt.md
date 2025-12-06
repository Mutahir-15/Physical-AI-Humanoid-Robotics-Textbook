---
id: 02
title: Analyze Project Artifacts
stage: general
date: 2025-12-05
surface: agent
model: gemini-1.5-pro-a
feature: none
branch: main
user: ADMINS
command: /sp.analyze Analyze /.specify/memory/constitution.md, /checklist and history/prompts.If all the details are accurate just let me know and I'll tell you the next move.
labels: ["analysis", "validation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
- checklists/technical-accuracy.md
- history/prompts/constitution/01-refine-constitution-mcp-server-clarification.constitution.prompt.md
- history/prompts/general/01-create-technical-accuracy-checklist.general.prompt.md
tests:
null
---

## Prompt

/sp.analyze Analyze /.specify/memory/constitution.md, /checklist and history/prompts.If all the details are accurate just let me know and I'll tell you the next move.

## Response snapshot

Reported that all analyzed artifacts (constitution, checklist, and relevant PHRs) were accurate and reflected the previous interactions.

## Outcome

- ✅ Impact: Confirmed accuracy of all specified project artifacts.
- 🧪 Tests: N/A
- 📁 Files: Analyzed .specify/memory/constitution.md, checklists/technical-accuracy.md, and relevant PHRs.
- 🔁 Next prompts: null
- 🧠 Reflection: Successfully performed a self-review of created artifacts and reported accuracy to the user, as requested.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
