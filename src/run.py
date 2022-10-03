#!/usr/bin/env python3
# ---
# Project Name: 
# Date Created: 
# Author: 
# Description: 
# 
# 
# Last Edited: 
# ---

import argparse
import pathlib
from datetime import datetime

from utils import logger

PATH_TO_TOP = f"{pathlib.Path(__file__).resolve().parent.parent}"

def main():
    """
    
    """
    log = logger.setup("log", level="debug", stream=True)
    log.info(f"Started at {datetime.now()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="integer argument to pass", default=0, type=int)
    parser.add_argument("-b", help="boolean argument to pass", action="store_true")
    args = parser.parse_args()

    main()