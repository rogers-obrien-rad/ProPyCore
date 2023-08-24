import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore

from dotenv import load_dotenv

if os.getenv("CLIENT_ID") is None:
    load_dotenv()

PATH_TO_TOP = f"{pathlib.Path(__file__).resolve().parent.parent}"

if __name__ == "__main__":
    connection = Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

    # Get IDs for company, project, and tool
    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    project = connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )
    tool = connection.__tools__.find_tool(
        company_id=company["id"],
        identifier="Idea Submission"
    )
    print("Company:", company["id"])
    print("Project:", project["id"])
    print("Tool:", tool["id"])

    # Example 1: create new idea submission status
    # ---------
    print("Example 1")
    # create data payload
    data = {
        "generic_tool_status": {
            "status_name": "In Review",
            "status": "Open"
        }
    }
    # create the item
    tool_status = connection.__tools__.delete_tool_status(
        company_id=company["id"],
        tool_id=tool["id"],
        data=data
    )
    # show created item
    print(tool_status)

    