import http.client
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    conn = http.client.HTTPSConnection("api.procore.com")
    body={"grant_type": "authorization_code",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "code": "Z4ddKJm9X1uRFcJRJZd9VuOPRef68iSDesf+7M3iUN/aXxGxpjzHEIeXiQWp/dGXQaLXH2vwR8f7oRha2tYHcg==",
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "refresh_token": "string"
    }

    headers = { "content-type": "application/json" }

    conn.request("POST", "/oauth/token", str(body), headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))