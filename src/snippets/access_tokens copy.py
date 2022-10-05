import requests
import requests.auth
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    #client_auth = requests.auth.HTTPBasicAuth(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
    post_data = {"grant_type": "authorization_code",
                 "client_id": os.getenv("CLIENT_ID"),
                 "client_secret": os.getenv("CLIENT_SECRET"),
                 "code": "Uhkx8IQRe7CbR3XkqyJ5mchP+G7kuei3lzTqCaum/DW4YDNCW82qGNHlGWYENfiSGNNtIYPHhp6AHyfAi5QQyg==",
                 "redirect_uri": os.getenv("REDIRECT_URI")
                 }
    response = requests.post(os.getenv("BASE_URL")+"/oauth/token",
                             data=post_data)
    response_json = response.json()

    print(response_json)
    print(response_json["access_token"])
    print(response_json["refresh_token"])
    print(response_json['created_at'])