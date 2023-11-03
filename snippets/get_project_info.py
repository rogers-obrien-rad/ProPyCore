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

    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    

    # Example 1: Get all projects with the app installed
    # ---------
    print("Example 1")
    projects = connection.__projects__.get(
        company_id=company["id"]
    )
    print(f"Number of projects: {len(projects)}")

    # Example 2: Find a specific project
    # ---------
    print("Example 2")
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="1301 South Lamar"
    )
    print(json.dumps(project, indent=4))

    