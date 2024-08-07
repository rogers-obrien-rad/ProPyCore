import os
import json
from dotenv import load_dotenv

from ProPyCore.procore import Procore
from ProPyCore.exceptions import NotFoundItemError

# Load environment variables from .env file if not already set
if os.getenv("CLIENT_ID") is None:
    load_dotenv()

if __name__ == "__main__":
    # Initialize the Procore connection
    connection = Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

    # Example 1: list available companies
    print("Example 1")
    companies = connection.__companies__.get()
    for company in companies:
        print(company["name"])
    # Expected output: Rogers-O`Brien Construction

    # Example 2: find company by name (str)
    print("\nExample 2")
    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    print(f"{company['id']}: {company['name']}")
    # Expected output: 8089: Rogers-O`Brien Construction
    print(json.dumps(company, indent=4))
    # See example in /references/

    # Example 3: find company by id (int)
    print("\nExample 3")
    company = connection.__companies__.find(identifier=8089)
    print(f"{company['id']}: {company['name']}")
    # Expected output: 8089: Rogers-O`Brien Construction

    # Example 4: non-existent company
    print("\nExample 4")
    try:
        company = connection.__companies__.find(identifier=1)
        print(company)
    except NotFoundItemError as e:
        print(e)
    # Expected output: 'Could not find company 1'
