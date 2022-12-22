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

    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )

    # create a folder
    connection.__folders__.create(
        company_id=company["id"],
        project_id=project["id"],
        folder_name=f"Folder_in_Root"
    )

    folder = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="Folder_in_Root"
    )

    # Example 1: Move folder
    # ---------
    print("Example 1")
    subfolder = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="I-Safety and Environmental"
    )

    connection.__folders__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=folder["id"],
        parent_id=subfolder["id"]
    )

    # Example 2: Update folder name
    # ---------
    print("\nExample 2")
    connection.__folders__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=folder["id"],
        folder_name="Now_a_Subfolder"
    )

    # Example 3: Change permissions
    # ---------
    print("\nExample 2")
    connection.__folders__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=folder["id"],
        private=True
    )