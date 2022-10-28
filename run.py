#!/usr/bin/env python3
# ---
# Project Name: ProPyCore
# Date Created: 10/04/2022
# Author: Hagen Fritz
# Description: Basic utility of the ProCore API with Python
# Last Edited: 10/25/2022
# ---

import argparse
import pathlib
import os

from datetime import datetime
from dotenv import load_dotenv

from propycore import procore
from propycore.utils import logger

# Load environment variables to populate Procore class
if os.getenv("CLIENT_ID") is None:
    load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET= os.getenv("CLIENT_SECRET")
REDIRECT_URI= os.getenv("REDIRECT_URI")
OAUTH_URL= os.getenv("OAUTH_URL")
BASE_URL= os.getenv("BASE_URL")

PATH_TO_TOP = f"{pathlib.Path(__file__).resolve().parent.parent}"

def main():
    """
    A display of the capabilities of the program
    """
    log = logger.setup("log", level="debug", stream=True)
    log.info(f"Started at {datetime.now()}")

    connection = procore.Procore(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        oauth_url=OAUTH_URL,
        base_url=BASE_URL
    )
    
    # Company
    company_list = connection.__companies__.get()
    company_test = company_list[0]["id"]
    log.info(f"Company: {company_test}")

    print(connection.find_company(identifier="DataPull"))

    # Project
    project_list = connection.__projects__.get(company_id=company_test)
    project_test = project_list[0]["id"]
    log.info(f"Project: {project_test}")
    print(connection.find_project(company_id=connection.find_company("DataPull")["id"],identifier="R&D Test Project"))

    # Folder and Files
    # ----------------
    # Create some files
    status_txt = connection.__files__.create(company_id=company_test, project_id=project_test, filepath="./data/test/test_txt.txt")
    log.info(status_txt)
    status_pdf = connection.__files__.create(company_id=company_test, project_id=project_test, description="A PDF file", filepath="./data/test/test_pdf.pdf")
    log.info(status_pdf)
    status_excel = connection.__files__.create(company_id=company_test, project_id=project_test, filepath="./data/test/test_excel.xlsx")
    log.info(status_excel)
    status_csv = connection.__files__.create(company_id=company_test, project_id=project_test, filepath="./data/test/test_csv.csv")
    log.info(status_csv)
    # create file in specified location
    dir_ids = connection.find_dir(
        company="DataPull",
        project="R&D Test Project",
        folderpath="/I-Safety and Environmental/3-Orientations and Training/Subcontractors Orientation"
    )
    log.info(dir_ids)
    status_specify = connection.__files__.create(company_id=company_test, project_id=project_test, parent_id=dir_ids[1], filepath="./data/test/test_pdf.pdf")
    log.info(status_specify)

    # Create a folder
    status = connection.__folders__.create(company_id=company_test, project_id=project_test, folder_name="Test Folder")
    log.info(status)

    # Folder/File List
    doc_list = connection.__folders__.root(company_id=company_test, project_id=project_test)

    root_folders = {}
    for folder in doc_list["folders"]:
        root_folders[folder["id"]] = folder["name"]
    log.info(f"Folders in Root: {root_folders}")

    root_files = {}
    for file in doc_list["files"]:
        root_files[file["id"]] = file["name"]
    log.info(f"Files in Root: {root_files}")

    # Folder info
    folder_test = list(root_folders.keys())[0]
    folder_info = connection.__folders__.show(company_id=company_test, project_id=project_test, doc_id=folder_test)
    subfolders = {"id":[],"name":[]}
    for subfolder in folder_info["folders"]:
        subfolders["id"].append(subfolder["id"])
        subfolders["name"].append(subfolder["name"])
    log.info(f"Subfolders in first folder: {subfolders}")

    # File info
    file_test = list(root_files.keys())[0]
    file_info = connection.__files__.show(company_id=company_test, project_id=project_test, doc_id=file_test)
    log.debug(file_info)

    # Delete some files
    #for file_id, file_name in root_files.items():
    #    status = connection.__files__.remove(company_id=company_test, project_id=project_test, doc_id=file_id)
    #    log.info(f"{status} - {file_name}")

    # Delete the Folder
    for folder_id, folder_name in root_folders.items():
        if folder_name == "Test Folder":
            status = connection.__folders__.remove(company_id=company_test, project_id=project_test, doc_id=folder_id)
            log.info(f"{status} - {folder_name}")
        else:
            log.info(f"Not deleting folder {folder_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="integer argument to pass", default=0, type=int)
    parser.add_argument("-b", help="boolean argument to pass", action="store_true")
    args = parser.parse_args()

    main()