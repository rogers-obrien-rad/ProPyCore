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

    # Example 1: Find file in root
    # ---------
    file1 = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="revu.png",
        look_for_file=True
    )
    print(f"{file1['id']}: {file1['name']}")

    # Example 2: Find file in subfolder
    # ----------
    file2 = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="Masonry Checklist.txt",
        look_for_file=True
    )
    print(f"{file2['id']}: {file2['name']}")

    # Example 3: No such file
    # ---------
    file3 = connection.find_doc(
        company_id=company["id"],
        project_id=project["id"],
        name="Not a file.txt",
        look_for_file=True
    )
    print(file3)
