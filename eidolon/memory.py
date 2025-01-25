import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from eidolon.config import Config
import datetime


def generate_local_embedding(text):
    # Connect to Ollama's embedding endpoint
    url = f"{Config.OLLAMA_API_URL}/api/embeddings"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "nomic-embed-text",
        "prompt": text
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        embedding = response.json().get('embedding')

        if not embedding:
            raise ValueError("No embedding returned from the model.")

        # Log the actual dimension
        embedding_length = len(embedding)
        print(f"Embedding generated with dimension: {embedding_length}")

        # Optionally validate dimensions dynamically if a minimum size is expected
        if embedding_length == 0:
            raise ValueError("Embedding has zero dimensions!")

        return embedding
    except requests.exceptions.RequestException as e:
        print(f"Error generating embedding: {e}")
        return None

def get_db_connection():
    return psycopg2.connect(Config.DB_URL, cursor_factory=RealDictCursor)

def get_relevant_context(query, limit=10):  # Set a higher default limit if needed
    connection = get_db_connection()
    cursor = connection.cursor()

    query_embedding = generate_local_embedding(query)
    if query_embedding is None:
        return "No relevant context available"

    cursor.execute(
        """
        SELECT content, timestamp
        FROM archival_memory
        ORDER BY embedding <#> %s::vector ASC
        LIMIT %s;
        """, (query_embedding, limit)  # Pass the limit parameter here
    )
    results = cursor.fetchall()
    connection.close()

    return "\n".join([f"[{row['timestamp']}] {row['content']}" for row in results])

def insert_into_db(content):
    connection = get_db_connection()
    cursor = connection.cursor()

    embedding = generate_local_embedding(content)
    if embedding is None:
        print("Failed to generate embedding, not storing in DB")
        return

    timestamp = datetime.datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO archival_memory (content, embedding, timestamp) VALUES (%s, %s, %s)",
        (content, embedding, timestamp)
    )
    connection.commit()
    cursor.close()
    connection.close()
