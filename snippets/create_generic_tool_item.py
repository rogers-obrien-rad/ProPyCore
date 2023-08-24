import os
import sys
import json
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore

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

    # Example 1: create new idea submission
    # ---------
    print("Example 1")
    # create data payload
    data = {
        "generic_tool_item": {
            "custom_field_378362": "This idea was submitted via API", # this field is unique
            "description": "None",
            "private": False,
            "received_from_id": 8780450, # this field is unique to your company
            "status":"Open",
            "title": "Idea Submited by API 3",
        }
    }
    # create the item
    tool_items = connection.__tools__.create_tool_item(
        company_id=company["id"],
        project_id=project["id"],
        tool_id=tool["id"],
        data=data
    )
    # show created item
    print(tool_items)