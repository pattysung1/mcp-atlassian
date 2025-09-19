import os
import sys
from dotenv import load_dotenv
from mcp_atlassian.confluence import ConfluenceFetcher
from mcp_atlassian.confluence.config import ConfluenceConfig

def main():
    """
    A simple script to test the Confluence search tool locally.
    Accepts a CQL query as a command-line argument.
    """
    # Load environment variables from .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        print(f"Loading .env file from: {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print("Warning: .env file not found.")

    # --- Configuration ---
    if len(sys.argv) > 1:
        SEARCH_CQL = sys.argv[1]
        print(f"Using CQL from command-line argument.")
    else:
        # Default example query
        SEARCH_CQL = 'space = "CJT" and title ~ "Test for dify and mcp"'
        print("Using default CQL query. You can provide your own as an argument.")
        print(f"Example: python {sys.argv[0]} 'space = \"MYSPACE\" and type = page'")

    print("--- Starting Confluence Search Tool Test ---")

    client = None
    try:
        # Initialize the Confluence client
        print("Initializing client...")
        config = ConfluenceConfig.from_env()
        if not config.url or not config.personal_token:
            raise ValueError("CONFLUENCE_URL and CONFLUENCE_PERSONAL_TOKEN must be set in .env")
        client = ConfluenceFetcher(config)
        print("Initialization successful!")
    except Exception as e:
        print(f"Failed to initialize client: {e}")
        return

    # --- Run the Search Test ---
    try:
        print(f"\nSearching Confluence with CQL: \"{SEARCH_CQL}\"\n")
        pages = client.search(cql=SEARCH_CQL, limit=5)

        if not pages:
            print("\n[INFO] Search returned no results.")
        else:
            print(f"\n[SUCCESS] Found {len(pages)} pages:")
            for page in pages:
                print(f"  - Title: {page.title}")
                print(f"    URL: {page.url}")
                # The content is the processed excerpt
                if page.content:
                    # Print first 100 chars of content
                    content_preview = page.content.strip().replace('\n', ' ')[:100]
                    print(f"    Content: {content_preview}...")
                print("-" * 20)

    except Exception as e:
        print(f"\n[FAILED] An error occurred during search: {e}")


if __name__ == "__main__":
    main()
