import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore

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
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )

    # Example 1: Find by ID
    # ---------
    print("Example 1")
    task1 = connection.__tasks__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier=86281591
    )

    print(task1["name"])

    # Example 2: Find by Title
    # ---------
    print("Example 2")
    task2 = connection.__tasks__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="BARKIN\' CREEK IMPROVEMENTS"
    )
    print(task2["id"])
    print(json.dumps(task2,indent=4))