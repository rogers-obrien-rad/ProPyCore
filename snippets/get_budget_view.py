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

    # Example 1: List all views
    # ---------
    print("Example 1")
    budget_views = connection.__budgets__.get_views(
        company_id=company["id"],
        project_id=project["id"]
    )

    print(f"Number of Budget Views: {len(budget_views)}")

    # Example 2: Find view by ID
    # ---------
    print("Example 2")
    budget_by_id = connection.__budgets__.find_view(
        company_id=company["id"],
        project_id=project["id"],
        identifier=406809
    )

    print(json.dumps(budget_by_id, indent=4))

    # Example 3: Find view by name
    # ---------
    print("Example 3")
    budget_by_name = connection.__budgets__.find_view(
        company_id=company["id"],
        project_id=project["id"],
        identifier="Simple Budget View"
    )

    print(json.dumps(budget_by_name, indent=4))