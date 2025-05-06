from dotenv import load_dotenv, find_dotenv
from aoe_rag import AoeRag

MESSAGE_WELCOME = "\n--- 👋 Willkommen bei AOE RAG ---"
MESSAGE_BYE = "\n✌️  Tschüss!\n"
MESSAGE_EXIT = "\nGib 'exit' oder 'quit' ein, um die Sitzung zu beenden."
MESSAGE_DESCRIPTION = (
    "\nDu kannst Fragen zu AOE stellen. "
    "Sie werden mit Hilfe von Informationen aus der AOE-Webseite beantwortet."
)

PROMPT_PREFIX = "\n👤 "
RESPONSE_PREFIX = "\n🤖 "


def main():
    load_dotenv(find_dotenv())

    rag = AoeRag()
    rag.initialize_index()

    # Interactive question loop
    print(MESSAGE_WELCOME)
    print(MESSAGE_DESCRIPTION)
    print(MESSAGE_EXIT)

    while True:
        question = input(PROMPT_PREFIX)

        # Check if user wants to exit
        if question.lower() in ["exit", "quit", "q"]:
            print(MESSAGE_BYE)
            break

        # Query the system and print the response
        if question.strip():  # Check if question is not empty
            response = rag.query(question)
            print(RESPONSE_PREFIX + response)


if __name__ == "__main__":
    main()
