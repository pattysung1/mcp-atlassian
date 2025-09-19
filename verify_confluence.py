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

# +------------------------------------------------------------------+
# |               <<< EDIT THIS VARIABLE FOR YOUR TEST >>>           |
# +------------------------------------------------------------------+
#  Set the Confluence Space Key you want to test.
#  The "Space Key" is usually a short identifier, e.g., 'PROJ', 'TEAM'.
#  For personal spaces, it's often '~username' or '~user_id'.
# TARGET_SPACE_KEY = "CJT"
# TARGET_SPACE_KEY = "~tony_chen5"
# TARGET_SPACE_KEY = "~PeiHsuan_Sung"
TARGET_SPACE_KEY = "CJT"

# +------------------------------------------------------------------+


def test_find_pages_in_space(client: ConfluenceFetcher, space_key: str):
    """Tests finding pages within a specific space."""
    print(f"\n--- Finding Pages in Space: '{space_key}' ---")

    try:
        # First, verify the space exists and we can access it
        print(f"Step A: Verifying access to space '{space_key}'...")
        all_spaces_response = client.get_spaces(limit=1000)
        all_spaces = all_spaces_response.get('results', [])
        
        target_space = None
        for s in all_spaces:
            if s['key'] == space_key:
                target_space = s
                break
        
        if not target_space:
            print(f"   [FAILED] Space with key '{space_key}' not found or you don't have permission to view it.")
            if all_spaces:
                print("\n   Available space keys you can see with your token:")
                for s in all_spaces:
                    print(f"     - Key: {s['key']}, Name: {s['name']}")
            else:
                print("   [INFO] Could not find any spaces with your current token.")
            return

        space_name = target_space.get('name', space_key)
        print(f"   [SUCCESS] Accessed space: '{space_name}'")

        # Now, search for pages within that space
        print(f"\nStep B: Searching for pages within space '{space_key}'...")
        cql = f'space = "{space_key}" and type = page'
        pages = client.search(cql=cql, limit=10)

        if not pages:
            print(f"   [INFO] Found no pages in space '{space_name}'.")
            return

        print(f"   [SUCCESS] Found {len(pages)} pages in '{space_name}'. Showing titles:")
        for page in pages:
            print(f"     - \"{page.title}\"")

    except Exception as e:
        print(f"   [FAILED] Error: {e}")

# --- Main Execution ---

def main():
    """Main function to run all tests."""
    print("--- Starting Confluence Connection Test ---")
    if not TARGET_SPACE_KEY:
        print("[ERROR] TARGET_SPACE_KEY is not set. Please edit the script.")
        return

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

    # Run the test
    test_find_pages_in_space(client, TARGET_SPACE_KEY)

if __name__ == "__main__":
    main()
