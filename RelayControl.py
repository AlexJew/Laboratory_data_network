import requests

myPlug = "192.168.0.152"
url = "http://"+myPlug+"/report"
response = requests.get(url)
data = response.json()  # automatically parses JSON
print(data)