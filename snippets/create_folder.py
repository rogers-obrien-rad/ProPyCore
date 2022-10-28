import os
import sys
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

    company = connection.find_company(identifier="DataPull")
    project = connection.find_project(company_id=company["id"], identifier="R&D Test Project")

    # Example 1: Create folder in Root (no parent_id provided)
    # ---------
    root_folder = connection.__folders__.create(
        company_id=company["id"],
        project_id=project["id"],
        folder_name="Folder_in_Root"
    )
    print(f"{root_folder['id']}: {root_folder['name']}")

    # Example 2: Create file in specified location
    # ---------
    folder = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="I-Safety and Environmental" # this needs to be a path in your procore project
    )
    
    subfolder = connection.__folders__.create(
        company_id=company["id"],
        project_id=project["id"],
        parent_id=folder["id"],
        folder_name="Subfolder"
    )
    print(f"{subfolder['id']}: {subfolder['name']}")