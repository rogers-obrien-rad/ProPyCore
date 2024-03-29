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

    # Example 1: Get company-level vendors
    # ---------
    print("Example 1")
    comp_users = connection.__users__.get(
        company_id=company["id"]
    )

    print("Number of users:", len(comp_users))
    print(json.dumps(comp_users[0],indent=4))
    # See example in /references/

    # Example 2: Get project-level users
    # ---------
    print("\nExample 2")
    # find project
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )

    proj_users = connection.__users__.get(
        company_id=company["id"],
        project_id=project["id"]
    )

    print("Number of users:", len(proj_users))
    print(json.dumps(proj_users[0],indent=4))
    # See example in /references/

