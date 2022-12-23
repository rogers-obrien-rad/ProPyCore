import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore
from propycore.exceptions import NotFoundItemError

from dotenv import load_dotenv
import json

if os.getenv("CLIENT_ID") is None:
    load_dotenv()

if __name__ == "__main__":
    connection = Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")

    # Example 1: Get trades
    # ---------
    print("Example 1")
    trades = connection.__trades__.get(company_id=company["id"])

    print("Number of trades:", len(trades))
    for trade in trades:
        print(trade["name"]) # limited number so we might as well print them out
    print(json.dumps(trades[0],indent=4))
    # See example in /references/

    # Example 2: Find trades
    # ---------
    print("\nExample 2")

    trade = connection.__trades__.find(
        company_id=company["id"],
        user_id="Acoustical Ceilings"
    )

    print(f"{trade['id']}: {trade['name']}")
    print(json.dumps(trade,indent=4))
    # See example in /references/

