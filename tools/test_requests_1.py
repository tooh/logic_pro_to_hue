import requests

url = "http://192.168.178.87/api/3ngO2dAvI7ImKdNqwUqcoaIKzbG8CcZfJAttky5i/lights/{}/state".format(1)

payload = " {\"on\":false}"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

r = requests.put(url, data=payload, headers=headers)
print(r.text)
