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

    # start by deleting the test files if they are present
    for old_file in ["test_pdf.pdf","renamed_test_pdf.pdf", "another_test_pdf.pdf"]:
        # look for the filename
        file_temp = connection.find_doc(
            company_id=company["id"],
            project_id=project["id"],
            name=old_file,
            look_for_file=True
        )
        # if the method returned something, delete that file
        if len(file_temp) != 0:
            response = connection.__files__.remove(
                company_id=company["id"],
                project_id=project["id"],
                doc_id=file_temp["id"],
            )
            print(f"Delete {old_file}:", response["status_code"])

    # create a file
    try:
        connection.__files__.create(
            company_id=company["id"],
            project_id=project["id"],
            filepath=f"{pathlib.Path(__file__).resolve().parent.parent}/data/test/test_pdf.pdf",
            description="Nothing to see here"
        )
    except ProcoreException:
        print("File already exists")

    file = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="test_pdf.pdf",
        look_for_file=True
    )

    # get file details - have to do this since the response from above does not include "description"
    file_original = connection.__files__.show(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file["id"]
    )

    # Example 1: Move file
    # ---------
    subfolder = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="I-Safety and Environmental"
    )

    file_new_loc = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file["id"],
        parent_id=subfolder["id"]
    )
    print(f"Original parent ID:", file["parent_id"])
    print(f"Updated parent ID:", file_new_loc["parent_id"])

    # Example 2: Update file name
    # ---------
    file_new_name = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file["id"],
        filename="renamed_test_pdf.pdf"
    )
    print(f"Original filename:", file["name"])
    print(f"Updated filename:", file_new_name["name"])

    # Example 3: Change Description
    # ---------
    file_new_desc = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file["id"],
        description="This document now has a fancy description"
    )
    print(f"Original description:", file_original["description"])
    print(f"Updated description:", file_new_desc["description"])

    # Example 4: Change permissions
    # ---------
    file_new_permissions = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file["id"],
        private=False
    )
    print(f"Private? (Original):", file["private"])
    print(f"Private? (Updated):", file_new_permissions["private"])

    # Example 5: Update file content
    # ---------
    file_new_content = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file["id"],
        filepath=f"{pathlib.Path(__file__).resolve().parent.parent}/data/test/another_test_pdf.pdf"
    )
    print("Original Number of Versions:", len(file_original["file_versions"]))
    print("Updated Number of Versions:", len(file_new_content["file_versions"]))