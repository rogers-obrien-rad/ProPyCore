import os
import sys
import json
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore
from propycore.exceptions import NotFoundItemError

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

    # Example 1: list all projects
    # ---------
    print("Example 1")
    projects = connection.__projects__.get(
        company_id=company["id"]
    )
    for project in projects:
        print(f"{project['id']}: {project['name']}")
    # 1668030: 1301 South Lamar
    # 291567: Sandbox Test Project

    # Example 2: find project by name (str)
    # ---------
    print("\nExample 2")
    project1 = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )
    print(f"{project1['id']}: {project1['name']}")
    # 291567: Sandbox Test Project
    print(json.dumps(project1, indent=4))
    # See example in /references/

    # Example 3: find project by id (int)
    # ---------
    print("\nExample 3")
    project2 = connection.__projects__.find(
        company_id=company["id"],
        identifier=1668030
    )
    print(f"{project2['id']}: {project2['name']}")
    # 1668030: 1301 South Lamar

    # Example 4: no such project
    # ---------
    print("\nExample 4")
    try:
        project3 = connection.__projects__.find(
            company_id=company["id"],
            identifier="Fake Project"
        )
        print(project3)
    except NotFoundItemError as e:
        print(e)
    # 'Could not find project Fake Project'