import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore
from propycore.exceptions import ProcoreException

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

    # Example 1: Create file in Root (no parent_id provided)
    # ---------
    try:
        file_in_root = connection.__files__.create(
            company_id=company["id"],
            project_id=project["id"],
            filepath=f"{pathlib.Path(__file__).resolve().parent.parent}/data/test/test_pdf.pdf"
        )
        print(f"{file_in_root['id']}: {file_in_root['name']}")
    except ProcoreException:
        print("Example 1: File already exists in root")

    # Example 2: Create file in specified location
    # ---------
    try:
        folder = connection.find_doc(
            company_id=company["id"],
            project_id=project["id"],
            name="Subcontractors Orientation" # this needs to be a folder in your procore project
        )

        file = connection.__files__.create(
            company_id=company["id"],
            project_id=project["id"],
            parent_id=folder["id"],
            filepath=f"{pathlib.Path(__file__).resolve().parent.parent}/data/test/test_pdf.pdf"
        )
        print(f"{file['id']}: {file['name']}")
    except ProcoreException:
        print("Example 2: File already exists in specified folder")