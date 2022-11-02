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

    company = connection.__companies__.find(identifier="DataPull")
    project = connection.__projects__.find(company_id=company["id"], identifier="R&D Test Project")

    # Example 1: Find folder in root
    # ---------
    folder1 = connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="F-Schedule"
    )
    print(f"{folder1['id']}: {folder1['name']}")

    # Example 2: Find subfolder
    # ----------
    folder2 = connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="Subcontractors Orientation"
    )
    print(f"{folder2['id']}: {folder2['name']}")

    # Example 3: No such folder
    # ---------
    try:
        folder3 = connection.__folders__.find(
            company_id=company["id"],
            project_id=project["id"],
            identifier="Not a folder"
        )
        print(folder3)
    except NotFoundItemError as e:
        print(e)
