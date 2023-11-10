import os
import pytest
import json
from dotenv import load_dotenv
from propycore.procore import Procore
from propycore.exceptions import NotFoundItemError

# Load environment variables from .env file for testing
load_dotenv()

@pytest.fixture(scope="module")
def procore_connection():
    return Procore(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        oauth_url=os.getenv("OAUTH_URL"),
        base_url=os.getenv("BASE_URL")
    )

def test_procore_integration(procore_connection):
    company = procore_connection.__companies__.find(identifier="Rogers-O`Brien Construction")
    project = procore_connection.__projects__.find(
        company_id=company["id"],
        identifier="Sandbox Test Project"
    )

    # Example 1: Find folder in root
    folder1 = procore_connection.__folders__.find(
        company_id=company["id"],
        project_id=project["id"],
        identifier="Z-Research and Development"
    )

    assert folder1 is not None
    assert folder1['id'] is not None
    assert folder1['name'] == "Z-Research and Development"