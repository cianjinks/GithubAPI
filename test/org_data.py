import requests
import os
import json

# List of top github organisations
orgs = ["microsoft", "google", "facebook", "apache", "alibaba", "vuejs", "tensorflow", "Tencent", "freeCodeCamp", "github"]

token = os.getenv('GITHUB_TOKEN', '...')
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'  
}

def get_org(org_name):
    url = f"https://api.github.com/orgs/{org_name}"
    r = requests.get(url, headers=headers)
    json_data = r.json()
    print(json.dumps(json_data, indent=4))
    return json_data

def get_org_repos(org_name):
    org = get_org(org_name)

    num_repos = org["public_repos"]
    print(f"{org_name} has {num_repos} repos: ")

    url = org["repos_url"]
    params = {"per_page": "100"}
    r = requests.get(url, headers=headers, params=params)
    json_data = r.json()

    repos = []
    for repo in json_data:
        name = repo["name"]
        repos.append(name)
        print(f"    {name}")
        
        stars = repo["stargazers_count"]
        forks = repo["forks_count"]
        open_issues = repo["open_issues"]
        print(f"        Stars - {stars}")
        print(f"        Forks - {forks}")
        print(f"        Open Issues - {open_issues}")

if __name__ == "__main__":
    get_org_repos(orgs[0])
    # get_org(orgs[0])