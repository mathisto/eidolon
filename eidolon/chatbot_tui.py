import requests
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style

# API Endpoint for your chatbot
API_URL = "http://127.0.0.1:8080/query"

# Terminal UI Style
style = Style.from_dict({
    "prompt": "bold green",
    "response": "italic",
    "error": "bold red",
})

def query_chatbot(user_query):
    """
    Send the user query to the chatbot API and return the response.
    """
    try:
        response = requests.post(
            API_URL,
            json={"user_query": user_query},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json().get("response", "No response received.")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    """
    Main function to run the chatbot terminal UI.
    """
    print("Welcome to Eidolon Chatbot! (Type 'exit' to quit)\n")
    session = PromptSession(history=InMemoryHistory())

    while True:
        try:
            user_query = session.prompt("You: ", style=style)
            if user_query.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            # Get response from chatbot
            chatbot_response = query_chatbot(user_query)
            print(f"Eidolon: {chatbot_response}")

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
