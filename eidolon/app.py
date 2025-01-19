from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from eidolon.llm_backend import query_llm
from eidolon.memory import get_relevant_context, insert_into_db

app = FastAPI()

# Define the request model
class QueryRequest(BaseModel):
    user_query: str

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        # Extract user query from the request model
        user_query = request.user_query

        # Retrieve relevant context from historical memory
        context = get_relevant_context(user_query)

        # Get response from the LLM using the user query and retrieved context
        response = query_llm(user_query, context)

        # Store both the user query and response into the memory database
        insert_into_db(user_query)
        insert_into_db(response)

        return {"response": response}

    except Exception as e:
        # Return a detailed HTTP exception on error
        raise HTTPException(status_code=500, detail=str(e))
