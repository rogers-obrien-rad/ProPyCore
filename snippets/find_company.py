import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore

from dotenv import load_dotenv

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

    # Example 1: find company by name (str)
    # ---------
    company = connection.find_company(
        identifier="DataPull"
    )
    print(f"{company['id']}: {company['name']}")

    # Example 2: find company by id (int)
    # ---------
    company = connection.find_company(
        identifier=3829471
    )
    print(f"{company['id']}: {company['name']}")

    # Example 3: non-existent company
    # ---------
    company = connection.find_company(
        identifier=1
    )
    print(company)
