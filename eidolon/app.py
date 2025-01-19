from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from eidolon.llm_backend import query_llm  # Update import to match your structure
from eidolon.memory import get_relevant_context

app = FastAPI()

# Define the request model
class QueryRequest(BaseModel):
    user_query: str

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        # Extract user query from the request model
        user_query = request.user_query
        context = get_relevant_context(user_query)
        response = query_llm(user_query, context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
