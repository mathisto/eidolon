from openai import OpenAI
import requests
from eidolon.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Query OpenAI LLM
def query_openai(prompt, context):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": prompt},
    ])
    return response.choices[0].message.content

# Query Ollama LLM
def query_ollama(prompt, context):
    url = Config.OLLAMA_API_URL + "/api/query"
    payload = {"prompt": f"{context}\n{prompt}"}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json().get("response", "Error: No response from Ollama")

# Main LLM query function
def query_llm(prompt, context):
    if Config.ACTIVE_LLM == "openai":
        return query_openai(prompt, context)
    elif Config.ACTIVE_LLM == "ollama":
        return query_ollama(prompt, context)
    else:
        raise ValueError("Invalid LLM backend configured")
