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
    tool = connection.__tools__.find_tool(
        company_id=company["id"],
        identifier="Idea Submission"
    )
    print("Company:", company["id"])
    print("Project:", project["id"])
    print("Tool:", tool["id"])

    # Example 1: Find by Title
    # ---------
    print("Example 1")
    item1 = connection.__tools__.find_tool_item(
        company_id=company["id"],
        project_id=project["id"],
        tool_id=tool["id"],
        identifier="Complex Idea Submited by API"
    )

    print(f'Found Idea: \'{item1["title"]}: {item1["id"]}\'')

    # Example 2: Find by ID
    # ---------
    print("Example 2")
    item2 = connection.__tools__.find_tool_item(
        company_id=company["id"],
        project_id=project["id"],
        tool_id=tool["id"],
        identifier=5020162
    )
    print(item2["id"])
    print(json.dumps(item2, indent=4))