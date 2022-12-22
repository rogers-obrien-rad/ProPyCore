import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore
from propycore.exceptions import NotFoundItemError, WrongParamsError

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

    # Housekeeping
    # ------------
    # start by deleting the test files if they are present
    for old_file in ["test_pdf.pdf", "renamed_test_pdf", "another_test_pdf.pdf"]:
        # look for the filename
        try:
            file_temp = connection.__files__.find(
                company_id=company["id"],
                project_id=project["id"],
                identifier=old_file
            )
            
            response = connection.__files__.remove(
                company_id=company["id"],
                project_id=project["id"],
                doc_id=file_temp["id"],
            )
            print(f"Delete {old_file}:", response["status_code"])
        except NotFoundItemError as e:
            print(e)

    # create a file
    try:
        connection.__files__.create(
            company_id=company["id"],
            project_id=project["id"],
            filepath=f"{pathlib.Path(__file__).resolve().parent.parent}/data/test/test_pdf.pdf",
            description="Nothing to see here"
        )
    except WrongParamsError as e:
        print(e)

    file_original = connection.__files__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="test_pdf.pdf"
    )

    # Example 1: Move file
    # ---------
    print("Example 1")
    subfolder = connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="I-Safety and Environmental"
    )

    file_new_loc = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file_original["id"],
        folder_id=subfolder["id"]
    )
    print(f"Original parent ID:", file_original["parent_id"])
    print(f"Updated parent ID:", file_new_loc["parent_id"])

    # Example 2: Update file name
    # ---------
    print("\nExample 2")
    file_new_name = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file_original["id"],
        filename="renamed_test_pdf.pdf"
    )
    print(f"Original filename:", file_original["name"])
    print(f"Updated filename:", file_new_name["name"])

    # Example 3: Change Description
    # ---------
    print("\nExample 3")
    file_new_desc = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file_original["id"],
        description="This document now has a fancy description"
    )
    print(f"Original description:", file_original["description"])
    print(f"Updated description:", file_new_desc["description"])

    # Example 4: Change permissions
    # ---------
    print("\nExample 4")
    file_new_permissions = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file_original["id"],
        private=False
    )
    print(f"Private? (Original):", file_original["private"])
    print(f"Private? (Updated):", file_new_permissions["private"])

    # Example 5: Update file content
    # ---------
    print("\nExample 5")
    file_new_content = connection.__files__.update(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file_original["id"],
        filepath=f"{pathlib.Path(__file__).resolve().parent.parent}/data/test/another_test_pdf.pdf"
    )
    print("Original Number of Versions:", len(file_original["file_versions"]))
    print("Updated Number of Versions:", len(file_new_content["file_versions"]))