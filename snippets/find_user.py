import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from ProPyCore.procore import Procore

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

    company = connection.companies.find(identifier="Rogers-O`Brien Construction")

    # Example 1: Get company-level user
    # ---------
    print("Example 1")
    comp_user = connection.directory.users.find(
        company_id=company["id"],
        user_id="Hagen Fritz"
    )

    print(f"{comp_user['id']}: {comp_user['name']}")
    print(json.dumps(comp_user,indent=4))
    # See example in /references/

    # Example 2: Get project-level users
    # ---------
    print("\nExample 2")
    # find project
    project = connection.projects.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )

    proj_user = connection.directory.users.find(
        company_id=company["id"],
        project_id=project["id"],
        user_id=8780450
    )

    print(f"{proj_user['id']}: {proj_user['name']}")
    print(json.dumps(proj_user,indent=4))
    # See example in /references/

