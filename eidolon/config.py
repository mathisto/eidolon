import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OLLAMA_API_URL = os.getenv("OLLAMA_BASE_URL", "http://100.108.91.106:11434")
    DB_URL = os.getenv("DATABASE_URL", "postgresql://mathisto:pugnare69@localhost:5432/eidolon")
    ACTIVE_LLM = os.getenv("ACTIVE_LLM", "openai")  # Options: "openai", "ollama"
