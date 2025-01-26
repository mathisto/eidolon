import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OLLAMA_API_URL = os.getenv("OLLAMA_BASE_URL")

    # Assemble the database URL using an environment variable for the password
    DATABASE_HOST = "localhost"
    DATABASE_PORT = "5432"
    DATABASE_NAME = "eidolon"
    DATABASE_USER = "eidolon"
    DATABASE_PASSWORD = os.getenv("EIDOLON_PG_PASS")  # Retrieve password from environment
    DB_URL = (
        f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@"
        f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )

    ACTIVE_LLM = os.getenv("ACTIVE_LLM", "openai")  # Options: "openai", "ollama"
