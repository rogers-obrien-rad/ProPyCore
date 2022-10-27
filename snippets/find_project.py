import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore
from snippets.find_company import find_company

from dotenv import load_dotenv

if os.getenv("CLIENT_ID") is None:
    load_dotenv()

def find_project(project_list, identifier):
    """
    Finds a company based on the identifier

    Parameters
    ----------
    project_list : list of dict
        projects from a specific company
    identifier : int or str
        project id number or company name
    
    Returns
    -------
    project : dict
        project-specific dictionary
    """
    if isinstance(identifier, int):
        key = "id"
    else:
        key = "name"

    for project in project_list:
        if project[key] == identifier:
            return project

    return {}

if __name__ == "__main__":
    connection = Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

    # get company called "DataPull"
    company_list = connection.__companies__.get()
    company = find_company(company_list, identifier="DataPull")
    
    # find the project "R&D Test Project"
    project_list = connection.__projects__.get(company_id=company["id"])
    project = find_project(project_list, "R&D Test Project")
    print(project)
