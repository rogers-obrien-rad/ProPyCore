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

    # Example 1: Find company-level vendor
    # ---------
    print("Example 1")
    comp_vendor = connection.__vendors__.find(
        company_id=company["id"],
        user_id="Procore (Test Companies)"
    )

    print(f"{comp_vendor['id']}: {comp_vendor['name']}")
    print(json.dumps(comp_vendor,indent=4))
    # See example in /references/

    # Example 2: Find project-level vendor
    # ---------
    print("\nExample 2")
    # find project
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )

    proj_vendor = connection.__vendors__.find(
        company_id=company["id"],
        project_id=project["id"],
        user_id=5181441
    )

    print(f"{proj_vendor['id']}: {proj_vendor['name']}")
    print(json.dumps(proj_vendor,indent=4))
    # See example in /references/

