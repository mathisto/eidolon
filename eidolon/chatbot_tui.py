import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

API_URL = "http://127.0.0.1:8080/query"
DEBUG_MODE = True

def query_chatbot(user_query):
    try:
        response = requests.post(
            API_URL,
            json={"user_query": user_query},
            headers={"Content-Type": "application/json"},
        )

        if DEBUG_MODE:
            print(f"DEBUG: {Fore.CYAN}Sending request to API...{Style.RESET_ALL}")
            print(f"DEBUG: Response status: {Fore.YELLOW}{response.status_code}{Style.RESET_ALL}")

        response.raise_for_status()
        return response.json().get("response", "No response received.")
    except requests.exceptions.RequestException as e:
        return f"{Fore.RED}Error: {e}{Style.RESET_ALL}"

def main():
    print("Welcome to Eidolon Chatbot! (Type 'exit' to quit)\n")

    while True:
        try:
            user_query = input("You: ")
            if user_query.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            # Get response from chatbot
            chatbot_response = query_chatbot(user_query)
            # Print response in a different color
            print(f"Eidolon: {Fore.GREEN}{chatbot_response}{Style.RESET_ALL}")

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
