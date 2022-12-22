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

    # Example 1: Find file in root
    # ---------
    print("Example 1")
    file1 = connection.__files__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="test_pdf.pdf"
    )
    print(f"{file1['id']}: {file1['name']}")
    # 607852186: test_pdf.pdf
    print(json.dumps(file1, indent=4))
    # See example in /references/

    # Example 2: Find file in subfolder
    # ----------
    print("\nExample 2")
    file2 = connection.__files__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="another_test_pdf.pdf"
    )
    print(f"{file2['id']}: {file2['name']}")
    # 607851830: another_test_pdf.pdf

    # Example 3: No such file
    # ---------
    print("\nExample 3")
    try:
        file3 = connection.__files__.find(
            company_id=company["id"],
            project_id=project["id"],
            identifier="Not a file.txt"
        )
        print(file3)
    except NotFoundItemError as e:
        print(e)
    # 'Could not find document Not a file.txt'
