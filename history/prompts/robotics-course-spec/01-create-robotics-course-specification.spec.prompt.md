---
id: 01
title: Create Robotics Course Specification
stage: spec
date: 2025-12-05
surface: agent
model: gemini-1.5-pro-a
feature: robotics-course-spec
branch: 001-robotics-course-spec
user: ADMINS
command: /sp.specify Generate a complete, detailed specification for the Docusaurus-based book titled: "Physical AI & Humanoid Robotics Course" Use the project constitution already created for this project. Follow all principles, standards, constraints, and success criteria strictly. The Specification MUST include: 1. **Book-Level Specification** - Target audience - Prerequisites - Learning goals - Tools and technologies required (ROS 2, Gazebo, Unity, NVIDIA Isaac, Whisper, Nav2, rclpy, etc.) - Overall structure of the book - Content style and tone guidelines (from constitution) - Deliverables for each module 2. **Module Specifications** For each of the 4 modules: - Module summary - Learning outcomes - Required software setup - Concepts covered - Mandatory examples, diagrams, or code snippets - Required simulation demos (Gazebo, Unity, Isaac) - ROS 2 integration points - Constraints (e.g., self-contained chapters, Docusaurus-ready MDX) Modules: 1. The Robotic Nervous System (ROS 2) 2. The Digital Twin (Gazebo & Unity) 3. The AI-Robot Brain (NVIDIA Isaac) 4. Vision-Language-Action (VLA) 3. **Chapter-Level Specifications** - Chapter titles for each module - Chapter purpose - Required diagrams / pseudo-code / exercises - Expected outputs for learners - Any API references or ROS 2 commands required - Simulation tasks associated with each chapter 4. **Capstone Project Specification** Define a full specification for the final project: “Autonomous Humanoid receiving voice → planning → navigation → object identification → manipulation” Must include: - Voice input pipeline (Whisper → LLM → ROS 2 actions) - Cognitive planning pipeline - Navigation pipeline (Isaac → VSLAM → Nav2) - Manipulation pipeline (URDF → controllers) - Evaluation criteria 5. **Documentation & Docusaurus Constraints** - Sidebar structure - Folder structure - Naming conventions - MDX formatting rules - How simulation files and diagrams must be referenced 6. **RAG Chatbot Future Integration Notes (Part 2)** (High-level specification only) - Text chunking strategy - Neon Postgres schema - Qdrant vector indexing - Chatbot contextual boundaries 7. **Acceptance criteria** - Matching the constitution principles - Self-contained, simulation-first, and MCP-deployable - Ready for `/sp.plan` generation Generate a highly structured, detailed, fully compliant specification.
labels: ["specification", "initial-spec"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- specs/001-robotics-course-spec/spec.md
- specs/001-robotics-course-spec/checklists/requirements.md
tests:
null
---

## Prompt

/sp.specify Generate a complete, detailed specification for the Docusaurus-based book titled: "Physical AI & Humanoid Robotics Course" Use the project constitution already created for this project. Follow all principles, standards, constraints, and success criteria strictly. The Specification MUST include: 1. **Book-Level Specification** - Target audience - Prerequisites - Learning goals - Tools and technologies required (ROS 2, Gazebo, Unity, NVIDIA Isaac, Whisper, Nav2, rclpy, etc.) - Overall structure of the book - Content style and tone guidelines (from constitution) - Deliverables for each module 2. **Module Specifications** For each of the 4 modules: - Module summary - Learning outcomes - Required software setup - Concepts covered - Mandatory examples, diagrams, or code snippets - Required simulation demos (Gazebo, Unity, Isaac) - ROS 2 integration points - Constraints (e.g., self-contained chapters, Docusaurus-ready MDX) Modules: 1. The Robotic Nervous System (ROS 2) 2. The Digital Twin (Gazebo & Unity) 3. The AI-Robot Brain (NVIDIA Isaac) 4. Vision-Language-Action (VLA) 3. **Chapter-Level Specifications** - Chapter titles for each module - Chapter purpose - Required diagrams / pseudo-code / exercises - Expected outputs for learners - Any API references or ROS 2 commands required - Simulation tasks associated with each chapter 4. **Capstone Project Specification** Define a full specification for the final project: “Autonomous Humanoid receiving voice → planning → navigation → object identification → manipulation” Must include: - Voice input pipeline (Whisper → LLM → ROS 2 actions) - Cognitive planning pipeline - Navigation pipeline (Isaac → VSLAM → Nav2) - Manipulation pipeline (URDF → controllers) - Evaluation criteria 5. **Documentation & Docusaurus Constraints** - Sidebar structure - Folder structure - Naming conventions - MDX formatting rules - How simulation files and diagrams must be referenced 6. **RAG Chatbot Future Integration Notes (Part 2)** (High-level specification only) - Text chunking strategy - Neon Postgres schema - Qdrant vector indexing - Chatbot contextual boundaries 7. **Acceptance criteria** - Matching the constitution principles - Self-contained, simulation-first, and MCP-deployable - Ready for `/sp.plan` generation Generate a highly structured, detailed, fully compliant specification.

## Response snapshot

The detailed specification for the "Physical AI & Humanoid Robotics Course" book has been successfully created and validated against the quality checklist. The specification is comprehensive, adheres to the project constitution, and is ready for the next phase.

## Outcome

- ✅ Impact: Detailed specification for the Robotics Course created and validated.
- 🧪 Tests: All items in the spec quality checklist passed.
- 📁 Files: Created specs/001-robotics-course-spec/spec.md and specs/001-robotics-course-spec/checklists/requirements.md.
- 🔁 Next prompts: Ready for /sp.plan.
- 🧠 Reflection: Successfully created a complex, multi-section specification and validated it against quality criteria, despite initial PowerShell script execution issues. Manually managed directory and branch creation.

## Evaluation notes (flywheel)

- Failure modes observed: Initial attempts to use `create-new-feature.ps1` failed due to PowerShell execution policy and complex string parsing. Successfully recovered by manually creating directories and branch, then using `write_file` for content.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
