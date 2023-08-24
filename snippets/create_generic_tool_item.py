import os
import sys
from datetime import datetime, timedelta
import random
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

    # Example 1: create new idea submission
    # ---------
    print("Example 1")
    # create simple data payload
    data = {
        "generic_tool_item": {
            "custom_field_378362": "This idea was submitted via API", # this field is unique
            "description": "None",
            "private": False,
            "received_from_id": 8780450, # this field is unique to your company
            "status":"Open",
            "title": "Simple Idea Submited by API",
        }
    }
    # create the item
    tool_item = connection.__tools__.create_tool_item(
        company_id=company["id"],
        project_id=project["id"],
        tool_id=tool["id"],
        data=data
    )
    # show created item
    print(tool_item)

    # Example 2: create new idea submission
    # ---------
    print("Example 2")
    # create more complex data payload
    data = {
        "generic_tool_item": {
            "assignee_ids": [
                8780450
            ],
            "attachments": [
                {
                "id": random.randint(1, 100),
                "url": "https://innovate.r-o.com",
                "filename": f"{PATH_TO_TOP}/references/sample_correspondence_file.pdf"
                }
            ],
            "cost_impact": "no_impact",
            "cost_impact_value": "none",
            "custom_field_378362": "This idea was submitted via API and includes more fields in the request body to keep things spicy.",
            "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "private": False,
            "received_from_id": 8780450,
            "schedule_impact": "no_impact",
            "schedule_impact_value": "none",
            "skip_emails": True,
            "status":"Open",
            "title": "Complex Idea Submited by API"
        }
    }
    # create the item
    tool_item = connection.__tools__.create_tool_item(
        company_id=company["id"],
        project_id=project["id"],
        tool_id=tool["id"],
        data=data
    )
    # show created item
    print(tool_item)