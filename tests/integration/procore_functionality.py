import os
from dotenv import load_dotenv

from src.propycore import procore

# Load environment variables to populate Procore class
if os.getenv("CLIENT_ID") is None:
    load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET= os.getenv("CLIENT_SECRET")
REDIRECT_URI= os.getenv("REDIRECT_URI")
OAUTH_URL= os.getenv("OAUTH_URL")
BASE_URL= os.getenv("BASE_URL")

def test_connection():
    connection = procore.Procore(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        oauth_url=OAUTH_URL,
        base_url=BASE_URL
    )
    assert connection is not None

def test_company_listing():
    connection = procore.Procore(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        oauth_url=OAUTH_URL,
        base_url=BASE_URL
    )
    temp_company_list = connection.__companies__.get()
    assert temp_company_list is list

def test_project_listing():
    connection = procore.Procore(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        oauth_url=OAUTH_URL,
        base_url=BASE_URL
    )
    company_list = connection.__companies__.get()
    temp_company = company_list[0]
    temp_projects = connection.__projects__.get(company_id=temp_company)
    assert temp_projects is list