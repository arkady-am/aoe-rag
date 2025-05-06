from dotenv import load_dotenv, find_dotenv
from aoe_rag import AoeRag


def main():
    # Load environment variables
    load_dotenv(find_dotenv())

    # Create RAG application (loads config.yaml by default)
    rag = AoeRag()

    # Initialize the index (create or load)
    rag.initialize_index()

    # Query the system
    response = rag.query("Was ist AOE?")
    print(response)


if __name__ == "__main__":
    main()
