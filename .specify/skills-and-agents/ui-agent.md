# UI Agent Definition

The UI Agent is the client-side orchestrator responsible for managing the interaction lifecycle between the user, the application state, and the visual presentation. It does not perform ML inference itself but applies logic to determine *how* intelligence is presented.

## Agent Metadata
- **Agent Name:** `InterfaceOrchestrator`
- **Role:** UX Logic Controller
- **Context:** Runs within the Docusaurus frontend (React State / Context).

## Responsibilities
1.  **State Interpretation:** Monitor user inputs, system status (loading, streaming, error), and backend metadata.
2.  **Skill Dispatch:** dynamic selection of the appropriate UI Skill (e.g., triggering `ContextAwareAnswerDisplay` vs. `EmptyStateIntelligence`).
3.  **Layout Adaptation:** Modifying the container classes and view modes based on content type.
4.  **Feedback Management:** Ensuring the user always knows system status and "why" a result occurred.

## Decision Flow

### Phase 1: Idle / Initialization
1.  **Check State:** Is chat history empty?
2.  **Decision:**
    - If YES -> Invoke **EmptyStateIntelligence**. Check current URL context to populate relevant suggestions.
    - If NO -> Render history, invoke **ContextAwareAnswerDisplay** for existing messages.

### Phase 2: Input & Intent Detection
1.  **Event:** User types in input box.
2.  **Action:** Invoke **QueryIntentClassifier** (debounce 300ms).
3.  **Decision:**
    - If `intent == 'how-to'` -> Pre-load "Instructions" skeleton loader.
    - If `intent == 'code'` -> Pre-load "Code Snippet" skeleton loader.
    - Else -> Standard loader.
4.  **Goal:** Provide immediate subconscious feedback that "I understand what kind of answer you need."

### Phase 3: Processing & Streaming
1.  **Event:** `submit_query`.
2.  **Action:** Transition UI to "Thinking" state. Show **RetrievalTraceViewer** placeholder if `judge_mode` is ON.
3.  **Event:** `stream_start`.
4.  **Action:** Invoke **ProgressiveAnswerReveal**.
    - Monitor incoming tokens.
    - If confidence metadata arrives early -> Invoke **AnswerConfidenceIndicator** immediately.
    - If retrieval paths arrive -> Populate **SourceGroundingHighlighter** data structures hiddenly.

### Phase 4: Answer Completion & Rendering
1.  **Event:** `stream_complete`.
2.  **Analysis:** Scan full answer text.
    - Does it contain citation markers? -> Activate **SourceGroundingHighlighter**.
    - Is it code heavy? -> Apply **ContextAwareAnswerDisplay** (Code Mode).
    - Is it short/factual? -> Apply **ExplanationFirstMode**.
3.  **Refinement:**
    - Calculate final confidence score. Update **AnswerConfidenceIndicator**.
    - If `judge_mode` -> Expand **RetrievalTraceViewer** with final JSON payload.

### Phase 5: Error Handling
1.  **Event:** `error_received`.
2.  **Strategy:**
    - Network Error -> Show "Retry" action + preserve user query in input.
    - No Context Found -> Invoke **EmptyStateIntelligence** (Fallback variant: "I couldn't find that in the docs. Here is what I *do* know...").

## Skill Invocation Order (Priority Stack)

1.  **Critical System Feedback:** (Network status, Error toasts) - *Highest Priority*
2.  **Streaming Logic:** (ProgressiveReveal)
3.  **Content Formatting:** (ContextAwareAnswer, ExplanationFirst)
4.  **Metadata Enrichment:** (SourceGrounding, ConfidenceIndicator)
5.  **Contextual Actions:** (SelectedTextMode) - *Lowest Priority / Passive*

## User Interaction States

| State | Visual Signal | Active Skills |
| :--- | :--- | :--- |
| **Idle (Empty)** | Clean slate, suggestion cards | `EmptyStateIntelligence` |
| **Typing** | Input active, intent icons fade in | `QueryIntentClassifier` |
| **Searching** | Progress bar / Skeleton UI | `QueryIntentClassifier` |
| **Streaming** | Cursor blinking, text fading in | `ProgressiveAnswerReveal` |
| **Reviewing** | Static text, interactive sources | `ContextAwareAnswerDisplay`, `SourceGroundingHighlighter` |
| **Inspecting** | Debug panel open, raw JSON visible | `RetrievalTraceViewer` |

## Improving UX without Visual Noise

- **Deterministic Stability:** The agent prevents layout shifts. By classifying intent *before* the answer arrives, it reserves the right amount of screen real estate.
- **Subtlety over Alert:** Confidence scores are color accents, not popups. Sources are integrated links, not massive footers (unless clicked).
- **Just-in-Time Context:** "Judge Mode" details are hidden by default, keeping the interface clean for general users but powerful for evaluators.
