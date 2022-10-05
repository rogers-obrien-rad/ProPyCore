import http.client
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    conn = http.client.HTTPSConnection("api.procore.com")
    
    headers = { 'Authorization': "Bearer " }

    conn.request("GET", "/rest/v1.0/companies", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))