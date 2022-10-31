import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore

from dotenv import load_dotenv
import json

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

    # Example 1
    # ---------
    file1 = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="revu.png",
        look_for_file=True
    )
    file1_info = connection.__files__.show(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file1["id"]
    )
    print(json.dumps(file1_info,indent=4))

    # Example 2
    # ---------
    file2 = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="test_pdf.pdf",
        look_for_file=True
    )
    file2_info = connection.__files__.show(
        company_id=company["id"],
        project_id=project["id"],
        doc_id=file2["id"]
    )
    print(json.dumps(file2_info,indent=4))