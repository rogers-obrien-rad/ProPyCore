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

    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )

    # Example 1
    # ---------
    print("Example 1")
    tasks1 = connection.__tasks__.get(
        company_id=company["id"],
        project_id=project["id"]
    )
    #for submittal in submittals:
    #    print(submittal["id"])

    print(f"Number of Tasks: {len(tasks1)}")
    print(json.dumps(tasks1[0],indent=4))