import requests
from datetime import datetime
import json

api_key="GdP46-rpcxB-2E6ZU-cGCg6"

now = datetime.now().strftime("%Y-%m-%d 00:00:00")
now10 = datetime.now().strftime("%Y-%m-%d 23:59:59")

params={ "types":"image","start":now,"end":now10,"_n":"1440","api_key":api_key }
url = "https://api.skaping.com/media/search"

r = requests.get(url, params=params)

rJSON = json.loads(r.text)
rJSON_Medias_Length = len(rJSON["medias"])

print(rJSON["medias"][rJSON_Medias_Length-1]["src"])