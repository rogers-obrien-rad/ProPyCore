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
    project = connection.find_project(company_id=company["id"], identifier="R&D Test Project")

    # Example 1: Find folder in root
    # ---------
    folder1 = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="F-Schedule",
        look_for_file=False
    )
    print(f"{folder1['id']}: {folder1['name']}")

    # Example 2: Find subfolder
    # ----------
    folder2 = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="Subcontractors Orientation",
        look_for_file=False
    )
    print(f"{folder2['id']}: {folder2['name']}")

    # Example 3: No such folder
    # ---------
    try:
        folder3 = connection.find_doc(
            company_id=company["id"],
            project_id=project["id"],
            name="Not a folder",
            look_for_file=False
        )
        print(folder3)
    except NotFoundItemError as e:
        print(e)
