# eidolon/__init__.py

from .app import app
from .config import Config
from .llm_backend import query_llm
from .memory import get_relevant_context, insert_into_db

__version__ = "0.1.0"
