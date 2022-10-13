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
        "response_type": "token",
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
    Gets access token from authorization code previously obtained from the get_auth_code call.
    
    Parameters
    ----------
    code : str
        temporary authorization code

    Returns
    -------
    <token> : str
        2-hour access token
    <created> : str
        time that the access token was created
    '''
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "client_credentials",
                "code": code,
                "redirect_uri": REDIRECT_URI
                }
    response = requests.post(BASE_URL+"/oauth/token", auth=client_auth, data=post_data)
    response_json = response.json()

    return response_json["access_token"], response_json['created_at']

if __name__ == "__main__":
    access_token, created_at = get_token("123")
    print(access_token)