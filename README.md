# Physical AI and Humanoid Robotics Textbook.

## RAG Chatbot Integration

This project integrates a Retrieval-Augmented Generation (RAG) chatbot into the Docusaurus-based robotics textbook. The chatbot leverages Gemini (LLM), Cohere (embeddings), Qdrant (vector store), and Neon Serverless Postgres (metadata store) to provide grounded answers to user queries based on the book's content.

### Project Structure

-   `backend/`: FastAPI application for ingestion, query, chat, and health endpoints.
    -   `backend/app/main.py`: Main FastAPI application.
    -   `backend/app/routers/`: API route definitions (ingest, query, chat, health).
    -   `backend/app/services/`: Business logic for embeddings, Qdrant, Neon DB, ingestion, and retrieval.
    -   `backend/app/agents/`: Gemini LLM interaction.
    -   `backend/app/db/`: Database schema (schema.sql).
    -   `backend/app/tests/`: Unit and integration tests.
    -   `backend/requirements.txt`: Python dependencies.
    -   `backend/.env.example`: Example environment variables for backend.
    -   `backend/Dockerfile`: Dockerfile for containerizing the backend.
-   `frontend/`: Contains the embeddable chat widget.
    -   `frontend/chat_widget/index.html`: The HTML structure of the chat widget.
    -   `frontend/chat_widget/client.js`: JavaScript logic for chat widget interaction and backend communication.
-   `docs/`: Docusaurus documentation (where the book content resides).
    -   `docs/rag_chatbot/`: Documentation specific to the RAG chatbot's design and implementation.
    -   `docs/chat/index.mdx`: Docusaurus page to embed the chat widget.
-   `scripts/`: Utility scripts.
    -   `scripts/sample_ingest_demo.py`: Sample script to demonstrate content cleaning and chunking.
    -   `scripts/ingest_all.py`: Script to trigger the full ingestion pipeline.
    -   `scripts/verify_index.py`: Script to verify Qdrant and Neon Postgres indices.
-   `.github/workflows/deploy-backend.yml`: GitHub Actions workflow for backend deployment.
-   `render.yaml`: Configuration for deploying the backend to Render.com.

### Local Development Setup

#### 1. Backend Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-org/spec-driven-online-hackathon-1.git
    cd spec-driven-online-hackathon-1
    ```

2.  **Create Python Virtual Environment**:
    ```bash
    python -m venv .venv/backend
    ./.venv/backend/Scripts/activate # On Windows
    source ./.venv/backend/bin/activate # On Linux/macOS
    ```

3.  **Install Python Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **Configure Environment Variables**:
    Copy `backend/.env.example` to `backend/.env` and fill in your API keys for Cohere, Qdrant, Neon, and Gemini. Also, set `INGESTION_API_KEY` to a strong secret.
    ```bash
    cp backend/.env.example backend/.env
    # Edit backend/.env with your actual keys
    ```

5.  **Start Neon Serverless Postgres**:
    Ensure your Neon Postgres database is set up and accessible via the `DATABASE_URL` in your `.env`.

6.  **Start Qdrant Cloud**:
    Ensure your Qdrant Cloud instance is set up and accessible via `QDRANT_URL` and `QDRANT_API_KEY` in your `.env`.

7.  **Initialize Database Schema**:
    First, ensure your `backend/.env` is correctly configured with `DATABASE_URL`.
    ```bash
    # Ensure you are in the virtual environment
    # You might need to adjust the path to your db.py
    python -c "import asyncio; from backend.app.services.db import NeonDBClient; async def init(): client = NeonDBClient(); await client.connect(); await client.initialize_schema(); await client.close(); asyncio.run(init())"
    ```
    *(Note: This command directly runs the schema initialization. In a more robust setup, you'd use a dedicated migration tool.)*

8.  **Run FastAPI Backend**:
    ```bash
    uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API documentation will be available at `http://localhost:8000/docs`.

#### 2. Ingest Content

Once the backend is running and the database schema is initialized:

1.  **Trigger Ingestion**:
    ```bash
    python scripts/ingest_all.py
    ```
    This script calls the `/ingest` endpoint of your running FastAPI backend, processing all `.mdx` files in your `docs/` directory, generating embeddings, and storing them in Qdrant and Neon Postgres.

2.  **Verify Index**:
    ```bash
    python scripts/verify_index.py
    ```
    This script will check if Qdrant and Neon Postgres contain the ingested data.

#### 3. Frontend Chat Widget

To see the chat widget locally within Docusaurus:

1.  **Install Docusaurus Dependencies**:
    ```bash
    npm install
    ```

2.  **Copy Chat Widget to Docusaurus Static Assets**:
    Docusaurus serves content from the `static/` directory. You need to copy the `frontend/chat_widget` contents there.
    ```bash
    cp -r frontend/chat_widget static/chat-widget-embed
    ```
    *(Note: For a production build, `docusaurus.config.js` might be configured to automatically pull from `frontend/chat_widget`.)*

3.  **Start Docusaurus Development Server**:
    ```bash
    npm run start
    ```
    Navigate to `http://localhost:3000/chat/` (or the equivalent path you configured for `docs/chat/index.mdx`) in your browser to see the embedded chatbot.

### Deployment

-   **Backend**: Refer to `backend/Dockerfile` for containerization and `render.yaml` for deployment to Render.com. Ensure all environment variables are securely configured on your chosen hosting platform.
-   **Frontend (Docusaurus)**: Deploy your Docusaurus site as usual (e.g., to GitHub Pages). Ensure the `chat-widget-embed` directory (from the local setup step) is correctly copied to the `static` directory during your Docusaurus build process for production. The GitHub Actions workflow `.github/workflows/deploy-backend.yml` provides a conceptual example for backend deployment.

### Testing

-   Basic unit tests for the backend are in `backend/app/tests/test_main.py`.
-   Run tests using `pytest` from the `backend/app` directory (after activating your virtual environment):
    ```bash
    pytest backend/app/tests/
    ```

---