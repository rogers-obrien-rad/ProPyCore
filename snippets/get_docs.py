import os
import sys
import urllib
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

    # Example 1: Get all folders
    # ---------
    print("Example 1")
    folders = connection.__folders__.get(
        company_id=company["id"],
        project_id=project["id"]
    )
    print(folders)

    # Example 2: Get all files
    # ---------
    print("\nExample 2")
    files = connection.__files__.get(
        company_id=company["id"],
        project_id=project["id"]
    )
    print(files)
    
    print("Number of folders:", len(folders))
    print("Number of files:", len(files))

    # Example 3: Get all children folders from parent
    # ---------
    print("\nExample 3")
    subfolders = connection.__folders__.get(
        company_id=company["id"],
        project_id=project["id"],
        folder_id=607848046
    )
    print(subfolders)

    # Example 4: Get all children files from parent
    # ---------
    print("\nExample 4")
    subfiles = connection.__files__.get(
        company_id=company["id"],
        project_id=project["id"],
        folder_id=607848046
    )
    print(subfiles)