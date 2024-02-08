import os
import pytest
from propycore.procore import Procore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fixture for Procore connection
@pytest.fixture
def procore_connection():
    return Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

def test_procore_integration(procore_connection):
    # Get IDs for company, project, and tool
    company = procore_connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    project = procore_connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )
    tool = procore_connection.__tools__.find_tool(
        company_id=company["id"],
        identifier="Idea Submission"
    )

    assert company is not None
    assert project is not None
    assert tool is not None

    # Example 1: list all items for idea submission tool
    tool_items = procore_connection.__tools__.get_tool_items(
        company_id=company["id"],
        project_id=project["id"],
        tool_id=tool["id"]
    )

    assert isinstance(tool_items, list)  # or any other assertion based on expected response