import os
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.procore import Procore
from propycore.exceptions import NotFoundItemError

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

    # Example 1: find tool by title
    # ---------
    print("Example 1")
    tool_by_id = connection.__tools__.find_tool(
        company_id=company["id"],
        identifier="Idea Submission"
    )
    print(f"{tool_by_id['id']}: {tool_by_id['title']}")
    # 378532: Idea Submission

    # Example 2: find tool by id (int)
    # ---------
    print("\nExample 2")
    tool_by_name = connection.__tools__.find_tool(
        company_id=company["id"],
        identifier=287343
    )
    print(f"{tool_by_name['id']}: {tool_by_name['title']}")
    # 287343: Change Request

    # Example 3: no such tool
    # ---------
    print("\nExample 3")
    try:
        no_tool = connection.__tools__.find_tool(
            company_id=company["id"],
            identifier="Fake Tool"
        )
    except NotFoundItemError as e:
        print(e)
    # 'Could not find tool Fake Tool'