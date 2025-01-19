from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import RealDictCursor
from eidolon.config import Config
import datetime

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your preferred model

def generate_embedding(text):
    return model.encode(text).tolist()

# Connect to the database
def get_db_connection():
    return psycopg2.connect(Config.DB_URL, cursor_factory=RealDictCursor)

# Fetch relevant context from memory
def get_relevant_context(query):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Generate query embedding
    query_embedding = generate_embedding(query)

    # Perform similarity search with explicit cast
    cursor.execute(
        """
        SELECT content, timestamp
        FROM archival_memory
        ORDER BY embedding <#> %s::vector ASC
        LIMIT 5;
        """, (query_embedding,)
    )
    results = cursor.fetchall()
    connection.close()

    # Format the retrieved context with timestamps
    return "\n".join([f"[{row['timestamp']}] {row['content']}" for row in results])


# Insert new data with timestamp
def insert_into_db(content):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Generate embedding for the content
    embedding = generate_embedding(content)
    timestamp = datetime.datetime.now().isoformat()

    # Insert into database
    cursor.execute(
        "INSERT INTO archival_memory (content, embedding, timestamp) VALUES (%s, %s, %s)",
        (content, embedding, timestamp)
    )
    connection.commit()
    cursor.close()
    connection.close()
