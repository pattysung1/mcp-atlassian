import os
from dotenv import load_dotenv
from mcp_atlassian.confluence import ConfluenceFetcher
from mcp_atlassian.confluence.config import ConfluenceConfig
from typing import Any, List, Optional

# Explicitly load .env file from the script's directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    print(f"Loading .env file from: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f".env file not found at: {dotenv_path}")

# --- Test Functions ---

def test_list_all_spaces(client: ConfluenceFetcher) -> Optional[List[Any]]:
    """Tests basic connectivity by listing all visible spaces."""
    print("\n--- Test 1: List All Visible Spaces ---")
    try:
        response = client.get_spaces(limit=50)
        spaces = response.get('results', [])
        if not spaces:
            print("   [WARNING] API call succeeded but no spaces were returned.")
            return None
        else:
            print(f"   [SUCCESS] Found {len(spaces)} spaces. Showing first 5:")
            for space in spaces[:5]:
                print(f"     - {space['name']} (Key: {space['key']})")
            return spaces
    except Exception as e:
        print(f"   [FAILED] Error: {e}")
        return None

def test_find_pages_in_space(client: ConfluenceFetcher, spaces: List[Any]):
    """Tests finding pages within the first available space."""
    print("\n--- Test 2: Find Page Titles in a Space ---")
    if not spaces:
        print("   [SKIPPED] No spaces found from the previous test.")
        return

    first_space = spaces[0]
    space_key = first_space['key']
    space_name = first_space['name']
    print(f"   Step A: Using first available space: '{space_name}' ({space_key})")

    try:
        print(f"\n   Step B: Searching for pages within space '{space_key}'...")
        cql = f'space = "{space_key}" and type = page'
        # The client.search method returns a list of page objects, not a dictionary
        pages = client.search(cql=cql, limit=5)

        if not pages:
            print(f"   [WARNING] Found no pages in space '{space_key}'.")
            return

        print(f"   [SUCCESS] Found {len(pages)} pages in '{space_name}'. Showing titles:")
        for page in pages:
            # The page object has a 'title' attribute
            print(f"     - \"{page.title}\"")

    except Exception as e:
        print(f"   [FAILED] Error: {e}")

# --- Main Execution ---

def main():
    """Main function to run all tests."""
    print("--- Starting Confluence Connection Test ---")
    client = None
    try:
        # Load configuration and create client
        print("Initializing client...")
        config = ConfluenceConfig.from_env()
        if not config.url or not config.personal_token:
            raise ValueError("CONFLUENCE_URL and CONFLUENCE_PERSONAL_TOKEN must be set.")
        client = ConfluenceFetcher(config)
        print("Initialization successful!")
    except Exception as e:
        print(f"Failed to initialize client: {e}")
        return

    # Run tests
    spaces = test_list_all_spaces(client)
    if spaces:
        test_find_pages_in_space(client, spaces)

if __name__ == "__main__":
    main()