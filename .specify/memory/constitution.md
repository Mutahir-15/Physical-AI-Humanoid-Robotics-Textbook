<!--
SYNC IMPACT REPORT
- Version: 0.0.0 -> 1.0.0
- Principles Added:
  - Principle 1: Technical Accuracy and Rigor
  - Principle 2: Practical, Simulation-First Learning
  - Principle 3: Clear and Consistent Content
  - Principle 4: Modular and Structured Design
  - Principle 5: Capstone-Driven Progression
- Sections Added: All (Initial creation)
- Sections Removed: None
- Templates Validated:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Project Constitution: Physical AI & Humanoid Robotics Course

This document outlines the foundational principles, standards, and governance for the "Physical AI & Humanoid Robotics Course" project. All contributors and project artifacts MUST adhere to this constitution.

## 1. Governance

- **Constitution Version**: 1.2.0
- **Ratification Date**: 2025-12-05
- **Last Amended Date**: 2025-12-06

### 1.1. Project Overview

#### 1.1.1. Project Name
Physical AI & Humanoid Robotics Course

#### 1.1.2. Project Purpose
Create a complete Docusaurus-based educational book. Content will be authored and managed via the Context7 MCP Server. The final site will be primarily deployed to GitHub Pages. The book covers four major modules:
1. The Robotic Nervous System (ROS 2)
2. The Digital Twin (Gazebo & Unity)
3. The AI-Robot Brain (NVIDIA Isaac)
4. Vision-Language-Action (VLA Robotics)

### 1.2. Amendment Process
Amendments to this constitution require a formal pull request and approval from at least one project maintainer. Approved changes MUST be accompanied by an update to the version number and the 'Last Amended Date'.

### 1.3. Versioning Policy
This constitution follows Semantic Versioning (MAJOR.MINOR.PATCH). MAJOR versions are for backward-incompatible changes, MINOR versions for adding or significantly altering principles, and PATCH versions for clarifications and typo fixes.

### 1.4. Compliance and Review
All project artifacts (Specifications, Plans, Tasks, and Implementations) created with Spec-Kit Plus MUST adhere to these principles. Compliance will be enforced during code and content reviews.

### 1.5. Deployment Policy (Updated)
- **Book creation and content management:** Context7 MCP Server will be used to author, structure, and manage the Docusaurus book.  
- **Primary deployment:** GitHub Pages will host the final Docusaurus site for public access.  
- **Integration rules:**  
    - All MDX files, assets, and simulation references must remain fully compatible with MCP Server integration.  
    - Deployment to GitHub Pages must not alter or remove any required MCP-specific structures, folders, or metadata.  
    - GitHub Pages hosting supersedes optional secondary deployment; it is now the main public-facing deployment platform.

---

## 2. Core Principles

These principles are the non-negotiable rules that govern all work on this project.

### Principle 1: Technical Accuracy and Rigor
All content MUST be technically precise, reflecting current best practices in robotics, simulation, and AI engineering. While the material is designed to be beginner-friendly, it MUST maintain academic and professional rigor.

### Principle 2: Practical, Simulation-First Learning
All learning materials MUST be practical and reproducible. Concepts MUST be grounded in hands-on, simulation-first exercises using standard industry tools like ROS 2, Gazebo, Unity, and the NVIDIA Isaac SDK. Real-world examples MUST be simulation-ready.

### Principle 3: Clear and Consistent Content
Explanations MUST be clear, professional, and have an engineering-focused tone. Humanoid-specific terminology MUST be used consistently. All complex topics MUST be supplemented with diagrams or pseudo-code. The final output MUST be compatible with Docusaurus Markdown (MDX).

### Principle 4: Modular and Structured Design
The book MUST be divided into 4 core modules, with each module containing lessons, exercises, diagrams, and simulation demos. Each chapter MUST be self-contained and managed through the Context7 MCP Server for content authoring and structuring. The final Docusaurus site MUST be optimized for deployment to GitHub Pages.

### Principle 5: Capstone-Driven Progression
All modules and lessons MUST progressively build the skills necessary for the final capstone project: "Autonomous Humanoid receiving voice -> action -> navigation -> manipulation". This ensures a goal-oriented learning path.