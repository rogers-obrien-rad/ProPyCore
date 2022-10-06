import urllib
import requests
from dotenv import load_dotenv
import os

from bs4 import BeautifulSoup

load_dotenv()

if __name__ == "__main__":
    params = {
        "client_id": os.getenv("CLIENT_ID"),
        "response_type": "code",
        "redirect_uri":  os.getenv("REDIRECT_URI")
    }
    url = os.getenv("OAUTH_URL") + "/oauth/authorize?" + urllib.parse.urlencode(params)
    response = requests.get(url, headers = { "content-type": "application/json" })
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all("meta"):
            if tag.get("name", None) == "csrf-token":
                auth_code = tag.get("content", None)