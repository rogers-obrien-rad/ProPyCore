import os
from dotenv import load_dotenv
import urllib
import requests

if os.getenv("CLIENT_ID") is None:
    load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET= os.getenv("CLIENT_SECRET")
REDIRECT_URI= os.getenv("REDIRECT_URI")
OAUTH_URL= os.getenv("OAUTH_URL")
BASE_URL= os.getenv("BASE_URL")

def get_companies(token, page=1, per_page=100):
    """
    
    """
    params = {
        "page": page,
        "per_page": per_page,
        "include_free_companies": True
    }
    url = BASE_URL + "/rest/v1.0/companies?" + urllib.parse.urlencode(params)
    print(url)

    response = requests.get(url, headers = { "Authorization": f"Bearer {token}" })
    print(response.status_code)
    response_json = response.json()
    print(response_json)

    return response