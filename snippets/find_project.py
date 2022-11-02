import os
import sys
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

    company = connection.find_company(identifier="DataPull")

    # Example 1: find project by name (str)
    # ---------
    project1 = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )
    print(f"{project1['id']}: {project1['name']}")

    # Example 2: find project by id (int)
    # ---------
    project2 = connection.find_project(
        company_id=company["id"],
        identifier=108707
    )
    print(f"{project2['id']}: {project2['name']}")

    # Example 3: no such project
    # ---------
    try:
        project3 = connection.find_project(
                company_id=company["id"],
                identifier="Fake Project"
        )
        print(project3)
    except NotFoundItemError as e:
        print(e)