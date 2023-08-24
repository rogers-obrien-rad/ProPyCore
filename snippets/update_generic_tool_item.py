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
    item = connection.__tools__.find_tool_item(
        company_id=company["id"],
        project_id=project["id"],
        tool_id=tool["id"],
        identifier="Idea Submited by API"
    )
    print("Company:", company["id"])
    print("Project:", project["id"])
    print("Tool:", tool["id"])
    print("Item:", item["id"])

    # Example 1: Change idea title
    # ---------
    print("Example 1")
    data = {
        "generic_tool_item": {
            "title": "Idea Submitted by API"
        }
    }
    updated_item = connection.__tools__.update_tool_item(
        company_id=company["id"],
        project_id=project["id"],
        tool_id=tool["id"],
        item_id=item["id"],
        data=data
    )
    print(f"Original title: {item['title']}\nUpdated title: {updated_item['title']}")