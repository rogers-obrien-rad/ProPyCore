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
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )

    # Example 1: Find folder in root
    # ---------
    print("Example 1")
    folder1 = connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="Z-Research and Development"
    )
    print(f"{folder1['id']}: {folder1['name']}")
    # 607848046: Z-Research and Development
    print(json.dumps(folder1, indent=4))
    # See example in /references/

    # Example 2: Find subfolder
    # ----------
    print("\nExample 2")
    folder2 = connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="Subcontractors Orientation"
    )
    print(f"{folder2['id']}: {folder2['name']}")
    # 607846791: Subcontractors Orientation

    # Example 3: No such folder
    # ---------
    print("\nExample 3")
    try:
        folder3 = connection.__folders__.find(
            company_id=company["id"],
            project_id=project["id"],
            identifier="Not a folder"
        )
        print(folder3)
    except NotFoundItemError as e:
        print(e)
    # 'Could not find document Not a folder'
