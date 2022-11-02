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

    company = connection.__companies__.find(identifier="DataPull")
    project = connection.__projects__.find(company_id=company["id"], identifier="Sandbox Test Project")

    # Example 1: Find rfi by number
    # ---------
    rfi1 = connection.__rfis__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="1",
    )
    print(f"{rfi1['id']}: {rfi1['number']}")
    print(json.dumps(rfi1,indent=4))

    # Example 2: Find rfi by id
    # ----------
    rfi2 = connection.__rfis__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier=43776
    )
    print(f"{rfi2['id']}: {rfi2['number']}")
    print(json.dumps(rfi2,indent=4))

    # Example 3: No such rfi
    # ---------
    try:
        rfi3 = connection.__rfis__.find(
            company_id=company["id"],
            project_id=project["id"],
            identifier=2
        )
        print(rfi3)
    except NotFoundItemError as e:
        print(e)
