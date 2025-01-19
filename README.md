Usage

Set Up Your Environment:

Install Python dependencies:

pip install -r requirements.txt

Ensure PostgreSQL is running with pgvector installed and configured.

Configure Environment Variables:

Set up the following variables in your .env file or system:

OPENAI_API_KEY=your_openai_api_key
OLLAMA_API_URL=http://100.108.91.106:11434
DATABASE_URL=postgresql://user:password@localhost:5432/eidolon
ACTIVE_LLM=openai  # Options: "openai", "ollama"

Run the Application:

Start the FastAPI server:

uvicorn app:app --reload

Access the API at http://127.0.0.1:8000.

Query the API:

Use /query endpoint to send a user query and receive enriched responses.

Example cURL:

curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d '{"user_query": "Hello!"}'

Database Management:

Use memory.py functions to insert and retrieve archival data.

Additional Documentation

Local Embeddings: Ensure SentenceTransformers is installed and integrated for efficient local embedding generation.

Metadata: Timestamps are stored and retrieved to provide historical context for responses.

Custom Backends: Modify config.py to add new LLM backends or customize existing ones.
