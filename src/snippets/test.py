import http.client

conn = http.client.HTTPSConnection("api.procore.com")

payload = "{\"grant_type\":\"authorization_code\",\"client_id\":\"5d8f339dbd6117a38087a347ca60c5aed0c472076e469d617cc553b33547e257\",\"client_secret\":\"629cdf69a99af405996861fd1559250d04ce1dc85b7eae22860c006966e8dd8f\",\"redirect_uri\":\"http://localhost\",\"refresh_token\":\"string\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))