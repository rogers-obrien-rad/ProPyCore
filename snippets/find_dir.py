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

def find_dir(connection, folderpath):
    """
    Traverses the Procore folder tree to find the given directory

    Parameters
    ----------
    connection : ProPycore connection obj
        API access to Procore
    folderpath : str
        full path (starting at root) to the final folder separated by forward-slashes ("/")
    
    Returns
    -------
    ids : list of int
        folder ids along the way to the specified folder
    """
    company = find_company(
        connection.__companies__.get(),
        identifier="DataPull"
    )

    project = find_project(
        connection.__projects__.get(company_id=company["id"]),
        identifier="R&D Test Project"    
    )

    # get root folder information
    root = connection.__folders__.root(
        company_id=company["id"],
        project_id=project["id"]
    )

    # removing any leading/trailing forward-slashes
    if folderpath[0] == "/":
        folderpath = folderpath[1:]
    if folderpath[-1] == "/":
        folderpath = folderpath[:-1]

    subfolders = folderpath.split("/")

    procore_folder_ids = []
    current_procore_folders = root["folders"]
    for subfolder in subfolders:
        folder_found_on_procore = False
        for procore_subfolder in current_procore_folders:
            if procore_subfolder["name"] == subfolder:
                procore_folder_ids.append(procore_subfolder["id"])
                folder_found_on_procore = True
                break

        if folder_found_on_procore:
            next_procore_folder = connection.__folders__.show(
                company_id=company["id"],
                project_id=project["id"],
                doc_id=procore_folder_ids[-1]
            )
            if next_procore_folder["has_children_folders"]:
                current_procore_folders = next_procore_folder["folders"]
            else:
                return procore_folder_ids
        else:
            return []

    return procore_folder_ids

if __name__ == "__main__":
    connection = Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

    # folderpath that exists on Procore with no children folders -> should return list of ints
    ids1 = find_dir(
        connection=connection,
        folderpath="/I-Safety and Environmental/3-Orientations and Training/Subcontractors Orientation"
    )

    # folderpath that exists on Procore with children folders -> should return list of ints
    ids2 = find_dir(
        connection=connection,
        folderpath="A-Drawings and Specs/1-Current"
    )

    # folderpath with file included -> should return the same list of ints as example 1
    ids3 = find_dir(
        connection=connection,
        folderpath="/I-Safety and Environmental/3-Orientations and Training/Subcontractors Orientation/test_txt.txt"
    )

    # incorrect folderpath -> should return empty list
    ids4 = find_dir(
        connection=connection,
        folderpath="/I-Safety and Environmental/3-Orientations and Training/Not a real folder/"
    )
