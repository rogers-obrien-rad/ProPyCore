import os
import json
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")
PATH_TO_FOLDER = pathlib.Path(__file__).resolve().parent

from ProPyCore.procore import Procore
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

    company = connection.companies.find(identifier="Rogers-O`Brien Construction")
    project = connection.projects.find(
        company_id=company["id"],
        identifier="1301 South Lamar"
    )
    print(company["id"])
    print(project["id"])

    # Example 1
    # ---------
    try:
        print("Example 1: List All Roles")
        all_roles = connection.directory.roles.list_all(
            company_id=company["id"]
        )
        print(f"Number of Roles: {len(all_roles)}")
        print(json.dumps(all_roles, indent=4))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2
    # ---------
    print("Example 2: Get Roles on a Project")
    project_roles = connection.directory.roles.get(
        company_id=company["id"],
        project_id=project["id"]
    )
    print(f"Number of Roles: {len(project_roles)}")
    print(json.dumps(project_roles, indent=4))

    # Example 3
    # ---------
    print("Example 3: Find a Person on a Project")
    project_role = connection.directory.roles.find(
        company_id=company["id"],
        project_id=project["id"],
        user_id="Brandon Arias (Rogers-O'Brien Construction Company)"
    )
    print(json.dumps(project_role, indent=4))