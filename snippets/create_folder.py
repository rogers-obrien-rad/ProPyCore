import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore
from propycore.exceptions import WrongParamsError

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

    # Example 1: Create folder in Root (no parent_id provided)
    # ---------
    print("Example 1")
    try:
        root_folder = connection.__folders__.create(
            company_id=company["id"],
            project_id=project["id"],
            folder_name="Z-Research and Development"
        )
        print(f"{root_folder['id']}: {root_folder['name']}")
    except WrongParamsError as e:
        print(e)
    # 607848046: Z-Research and Development

    # Example 2: Create folder in specified location
    # ---------
    print("\nExample 2")
    folder = connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="Z-Research and Development" # this needs to be a path in your procore project
    )
    # 607848083: A-Team
    
    try:
        subfolder = connection.__folders__.create(
            company_id=company["id"],
            project_id=project["id"],
            folder_id=folder["id"],
            folder_name="A-Team"
        )
        print(f"{subfolder['id']}: {subfolder['name']}")
    except WrongParamsError as e:
        print(e)

    # Example 3: Folder already exists
    # ---------
    print("\nExample 3")
    try:
        existing_folder_name = "I-Safety and Environmental"
        existing_folder = connection.__folders__.create(
            company_id=company["id"],
            project_id=project["id"],
            folder_name=existing_folder_name
        )
        print(f"{existing_folder['id']}: {existing_folder['name']}")
    except WrongParamsError as e:
        print(e)
    # 'Folder I-Safety and Environmental already exists'