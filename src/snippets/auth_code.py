import http.client
import urllib
import requests
from dotenv import load_dotenv
import os
import json

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
        print(response.text)

    code = "Uhkx8IQRe7CbR3XkqyJ5mchP+G7kuei3lzTqCaum/DW4YDNCW82qGNHlGWYENfiSGNNtIYPHhp6AHyfAi5QQyg=="