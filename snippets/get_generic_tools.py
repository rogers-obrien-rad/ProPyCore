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

    company = connection.__companies__.find(identifier="Rogers-O`Brien Construction")

    # Example 1: list all generic tools
    # ---------
    print("Example 1")
    tools = connection.__tools__.get_tools(
        company_id=company["id"]
    )
    for tool in tools:
        print(f"{tool['id']}: {tool['title']}")

    # 287343: Change Request
    # 140850: Cleanup Notice
    # 287380: Field Change
    # 140852: General Correspondence
    # 378532: Idea Submission
    # 140851: Letters
    # 344626: Letters of Intent
    # 140853: Notice of Delay
    # 140854: Notice to Proceed
    # 344627: Notification of Backcharge
    # 261716: Vendor Setup

    try:
        idea_submission_id = 378532
        idea_submission_tool = next(item for item in tools if item["id"] == idea_submission_id)
        print(json.dumps(idea_submission_tool, indent=4))
    except StopIteration:
        print("No such tool with id", idea_submission_id)