import requests
import os
import json
from pprint import pprint

token = os.getenv('GITHUB_TOKEN', '...')
owner = "guillaumechereau"
repo = "goxel"
query_url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
params = {
}
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'  
}
r = requests.get(query_url, headers=headers, params=params)
json_data = r.json()
print(f"There are {len(json_data)} contributors:")

for i in range(len(json_data)):
    print(f"{i+1}: {json_data[i]['login']} - {json_data[i]['contributions']}")