import os
from bs4 import BeautifulSoup
import requests
import urllib

from dotenv import load_dotenv

if os.getenv("CLIENT_ID") is None:
    load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET= os.getenv("CLIENT_SECRET")
REDIRECT_URI= os.getenv("REDIRECT_URI")
OAUTH_URL= os.getenv("OAUTH_URL")
BASE_URL= os.getenv("BASE_URL")

def get_auth_code():
    """
    Gets the 10-minute temporary authorization code
    """
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri":  REDIRECT_URI
    }
    url = OAUTH_URL + "/oauth/authorize?" + urllib.parse.urlencode(params)

    response = requests.get(url, headers = { "content-type": "application/json" })
    if response.status_code == 200:
        # use BS to parse the code from the returned html
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all("meta"):
            if tag.get("name", None) == "csrf-token":
                auth_code = tag.get("content", None)

    return auth_code

def get_token(code):
    '''
    DESCRIPTION:
        Gets the access token by utilizating the authorization code that was
        previously obtained from the authorization_url call.
    INPUTS:
        code = authorization code
    OUTPUTS:
        response_json["access_token"]  = user's current access token
        response_json["refresh_token"] = user's current refresh token
        response_json['created_at']    = the date and time the user's access
        token was generated
    '''
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI
                }
    response = requests.post(BASE_URL+"/oauth/token", auth=client_auth, data=post_data)
    response_json = response.json()
    print(response_json)

    return response_json["access_token"], response_json["refresh_token"], response_json['created_at']