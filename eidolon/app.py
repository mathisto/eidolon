import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from eidolon.llm_backend import query_llm
from eidolon.memory import get_relevant_context, insert_into_db
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

class OpenAIQueryRequest(BaseModel):
    model: str
    messages: list
    temperature: float = 1.0
    max_tokens: int = 150

models_data = [
    {"id": "gpt-3.5-turbo", "object": "model", "created": 1638493088, "owned_by": "openai", "permission": []},
    {"id": "gpt-4", "object": "model", "created": 1640992088, "owned_by": "openai", "permission": []},
    {"id": "gpt-4o", "object": "model", "created": 1643594088, "owned_by": "openai", "permission": []}
]

@app.get("/v1/models")
async def get_models():
    try:
        logging.debug("Fetching models data")
        return {"data": models_data, "object": "list"}
    except Exception as e:
        logging.error(f"Error fetching models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
async def openai_compatible_query_endpoint(request: OpenAIQueryRequest):
    try:
        user_query = ""
        for message in request.messages:
            if message.get("role") == "user":
                user_query = message.get("content", "")
                break

        logging.debug(f"User query received: {user_query}")

        context = get_relevant_context(user_query)
        logging.debug(f"Context retrieved: {context}")

        response_content = query_llm(user_query, context)
        logging.debug(f"Response from LLM: {response_content}")

        insert_into_db(user_query)
        insert_into_db(response_content)
        logging.debug("User query and response inserted into database")

        response = {
            "id": "some-unique-id",
            "object": "chat.completion",
            "created": int(datetime.now().timestamp()),
            "model": request.model,
            "choices": [
                {"index": 0, "message": {"role": "assistant", "content": response_content}, "finish_reason": "stop"}
            ],
            "usage": {
                "prompt_tokens": len(user_query.split()),
                "completion_tokens": len(response_content.split()),
                "total_tokens": len(user_query.split()) + len(response_content.split())
            }
        }

        return response

    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
