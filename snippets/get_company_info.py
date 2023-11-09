import os
import sys
import json
import urllib
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

    # Example 1: Get all companies with the app installed
    # ---------
    print("Example 1")
    companies = connection.__companies__.get()
    print(json.dumps(companies, indent=4))

    # Example 2: Find a specific company
    # ---------
    print("Example 2")
    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    print(json.dumps(company, indent=4))

    # Example 3: Get company projects
    projects = connection.__companies__.get_projects(
        company_id=company["id"]
    )
    print(f"Number of projects: {len(projects)}")
    print(json.dumps(projects[1], indent=4))

    # Example 4: Get project regions
    # ---------
    print("Example 4")
    regions = connection.__companies__.get_regions(
        company_id=company["id"]
    )
    print(json.dumps(regions, indent=4))

    # Example 5: Get project types
    # ---------
    print("Example 5")
    project_types = connection.__companies__.get_project_types(
        company_id=company["id"]
    )
    print(json.dumps(project_types, indent=4))