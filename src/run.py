#!/usr/bin/env python3
# ---
# Project Name: ProPyCore
# Date Created: 10/04/2022
# Author: Hagen Fritz
# Description: Basic utility of the ProCore API with Python
# Last Edited: 10/06/2022
# ---

import argparse
import pathlib
from datetime import datetime

from utils import logger
from procore import auth

PATH_TO_TOP = f"{pathlib.Path(__file__).resolve().parent.parent}"

def main():
    """
    
    """
    log = logger.setup("log", level="debug", stream=True)
    log.info(f"Started at {datetime.now()}")
    auth_code = auth.get_auth_code()
    print(auth_code)
    access, refresh, created = auth.get_token(auth_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="integer argument to pass", default=0, type=int)
    parser.add_argument("-b", help="boolean argument to pass", action="store_true")
    args = parser.parse_args()

    main()