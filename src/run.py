#!/usr/bin/env python3
# ---
# Project Name: ProPyCore
# Date Created: 10/04/2022
# Author: Hagen Fritz
# Description: Basic utility of the ProCore API with Python
# Last Edited: 10/12/2022
# ---

import argparse
import pathlib
import os

from datetime import datetime
from dotenv import load_dotenv

from propycore import procore
from propycore.access import base
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
    company_list = connection.__companies__.get()
    company_test = company_list[0]["id"]
    project_test = connection.__projects__.get(company_id=company_test)
    print(project_test)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="integer argument to pass", default=0, type=int)
    parser.add_argument("-b", help="boolean argument to pass", action="store_true")
    args = parser.parse_args()

    main()