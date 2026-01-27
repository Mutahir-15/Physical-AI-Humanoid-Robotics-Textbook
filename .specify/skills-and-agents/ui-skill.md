# UI Skills Catalog

This document defines reusable UI skills that enhance the intelligence, clarity, and responsiveness of the Docusaurus-based chatbot interface. These skills are invoked by the UI Agent to adapt the interface to user intent and system state.

## 1. ContextAwareAnswerDisplay

- **Intent:** Optimize the rendering of the answer based on the content type (e.g., code-heavy, conceptual, step-by-step).
- **Trigger Condition:** `answer_received` event produces a valid markdown response.
- **Input Signals:**
    - `answer_text`: The raw markdown content.
    - `contains_code`: Boolean.
    - `length`: Character count.
    - `structure_type`: 'list', 'paragraph', 'mixed'.
- **UI Behavior:**
    - If `structure_type` is 'list' (step-by-step), render as a specialized checklist or timeline view for clarity.
    - If `contains_code`, auto-expand the code block width and provide a "Copy" and "Run" (if applicable) action.
    - If long conceptual text, utilize "Read More" folding or section headings to prevent wall-of-text fatigue.
- **Reusability Scope:** Chat Message Component, Search Result Preview.
- **Failure / Fallback Behavior:** Render standard Markdown.

## 2. SourceGroundingHighlighter

- **Intent:** Visually link assertions in the answer to their specific source documents to build trust and facilitate deep dives.
- **Trigger Condition:** Answer contains citations `[doc_id]` or `[source]` AND `source_documents` metadata is available.
- **Input Signals:**
    - `citation_tokens`: Indices of citation markers in the text.
    - `source_metadata`: List of source objects (title, URL, snippet).
- **UI Behavior:**
    - Render citations as interactive chips/badges.
    - **Hover:** Show a tooltip with the specific relevant text snippet from the source.
    - **Click:** Scroll the adjacent documentation viewer (if split-screen) to the exact paragraph or open the source in a new tab.
    - Highlight the corresponding source card in the "Sources" section when hovering the text citation.
- **Reusability Scope:** Chat Interface, Summary Widgets.
- **Failure / Fallback Behavior:** Render static text `[1]`.

## 3. AnswerConfidenceIndicator

- **Intent:** Transparently communicate the system's certainty to manage user expectations and "hallucination" risk.
- **Trigger Condition:** Backend provides `retrieval_score` or `confidence_score` metadata with the answer.
- **Input Signals:**
    - `score` (float 0.0 - 1.0).
    - `thresholds`: Configured cutoffs for Low/Medium/High.
- **UI Behavior:**
    - **High (>0.85):** subtle green accent or "Verified Source" icon.
    - **Medium (0.6 - 0.85):** Neutral presentation.
    - **Low (<0.6):** Display a "Low Confidence" warning banner: *"This answer is generated with limited context. Please verify with linked sources."*
    - Adjust the tone of the "Sources" header (e.g., "Related Reading" instead of "Sources Used").
- **Reusability Scope:** Message Footer, Metadata Panel.
- **Failure / Fallback Behavior:** Hide indicator (neutral).

## 4. QueryIntentClassifier (Client-Side)

- **Intent:** Heuristically detect what the user wants to *do* to pre-configure the response layout before the full answer arrives.
- **Trigger Condition:** User types in input field or submits query.
- **Input Signals:**
    - `query_text`: The user's input string.
    - `regex_patterns`:
        - *How-to:* `^(how to|guide|steps|tutorial).*`
        - *Definition:* `^(what is|define|explain).*`
        - *Troubleshooting:* `^(error|fail|bug|fix|exception).*`
- **UI Behavior:**
    - **How-to:** Prepare a "Step-by-Step" layout template.
    - **Definition:** Prepare a "Concept Card" layout.
    - **Troubleshooting:** Prepare a layout with "Solution" and "Root Cause" distinct sections.
- **Reusability Scope:** Input Bar, Loading Skeleton, Response Container.
- **Failure / Fallback Behavior:** Default "General Conversation" layout.

## 5. ProgressiveAnswerReveal

- **Intent:** Reduce cognitive load by streaming the answer in logical chunks rather than a raw character stream, maintaining UI stability.
- **Trigger Condition:** Streaming response is active.
- **Input Signals:**
    - `stream_chunk`: Incoming text token.
    - `current_buffer`: Accumulated text.
- **UI Behavior:**
    - Buffer tokens until a sentence, list item, or code line break is complete.
    - Fade-in complete blocks of thought (sentences/paragraphs) rather than jittery character-by-character typing.
    - Auto-scroll only when a new logical block starts to prevent "reading chase."
- **Reusability Scope:** Streaming Text Renderer.
- **Failure / Fallback Behavior:** Standard character streaming.

## 6. EmptyStateIntelligence

- **Intent:** Guide the user to value immediately when no chat history exists, avoiding "Blank Page Syndrome."
- **Trigger Condition:** `chat_history.length === 0`.
- **Input Signals:**
    - `page_context`: Current documentation page user is viewing (if applicable).
    - `popular_queries`: Static list of high-value capabilities.
- **UI Behavior:**
    - Display 3-4 "Suggested Actions" cards relevant to the *current* documentation context (e.g., if reading about "Ingestion", suggest "How do I ingest a PDF?").
    - Show a brief "System Capabilities" summary (e.g., "I can explain code, summarize docs, and debug errors").
- **Reusability Scope:** Chat Widget initialization, New Chat Screen.
- **Failure / Fallback Behavior:** Show generic greeting "How can I help you?".

## 7. RetrievalTraceViewer (Judge Mode)

- **Intent:** Provide transparency into the RAG pipeline for developers and hackathon judges to verify "under the hood" logic.
- **Trigger Condition:** `debug_mode` enabled or `judge_view` toggle active.
- **Input Signals:**
    - `retrieval_payload`: JSON of query vectors, matched chunks, similarity scores.
    - `system_prompt`: The actual prompt sent to the LLM.
- **UI Behavior:**
    - Render a collapsible "Debug Info" accordion below the answer.
    - Visualizes the "Retrieved Chunks" with their raw scores.
    - Shows the exact "Context Window" used.
    - Highlights dropped/filtered chunks.
- **Reusability Scope:** Message Footer, Developer Settings.
- **Failure / Fallback Behavior:** Hide component.

## 8. SelectedTextContextMode

- **Intent:** Allow users to ask questions specifically about text they are reading in the main documentation window.
- **Trigger Condition:** User highlights text in the Docusaurus article page.
- **Input Signals:**
    - `selection_text`: The string highlighted.
    - `selection_location`: Page URL and paragraph ID.
- **UI Behavior:**
    - A "Ask AI about this" tooltip appears near the cursor.
    - Clicking it opens the Chat Widget and pre-fills the context: *"Regarding '[Selected Text]': [Cursor Focus]"*.
    - The chat session temporarily scopes retrieval boost to the current page.
- **Reusability Scope:** Global Docusaurus Layout.
- **Failure / Fallback Behavior:** Standard browser selection behavior.

## 9. ExplanationFirstMode

- **Intent:** Ensure answers prioritize direct explanation over fluff, adapting structure based on query complexity.
- **Trigger Condition:** `query_complexity` is High OR `user_preference` is "Concise".
- **Input Signals:**
    - `answer_sections`: Introduction, Body, Conclusion.
- **UI Behavior:**
    - Detect the "Bottom Line Up Front" (BLUF) sentence.
    - Render the BLUF in bold or a distinct "Summary" box at the very top.
    - Place detailed elaboration and background context in a secondary visual hierarchy (e.g., slightly smaller text or gray background).
- **Reusability Scope:** Answer Renderer.
- **Failure / Fallback Behavior:** Standard linear rendering.
