import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore
from snippets.find_company import find_company
from snippets.find_project import find_project

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

    company = find_company(
        connection.__companies__.get(),
        identifier="DataPull"
    )

    project = find_project(
        connection.__projects__.get(company_id=company["id"]),
        identifier="R&D Test Project"    
    )

    connection.__files__.create(
        company_id=company["id"],
        project_id=project["id"],
        filepath=f"{pathlib.Path(__file__).resolve().parent.parent}/data/test/pdf.pdf"
    )