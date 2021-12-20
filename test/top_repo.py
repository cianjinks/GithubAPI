import requests
import os
import json

# Top 10 repositories (https://gitstar-ranking.com/)
repos = {
    "freeCodeCamp": "freeCodeCamp",
    "996icu": "996.ICU",
    "EbookFoundation": "free-programming-books",
    "jwasham": "coding-interview-university",
    "vuejs": "vue",
    "facebook": "react",
    "kamranahmedse": "developer-roadmap",
    "sindresorhus": "awesome",
    "tensorflow": "tensorflow",
    "twbs": "bootstrap"
}

token = os.getenv('GITHUB_TOKEN', '...')
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_repo(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    r = requests.get(url, headers=headers)
    repo_data = r.json()

    print(f"Contributors of {owner}/{repo}")
    for contributor in repo_data:
        user = contributor["login"]
        total_contributions = contributor["contributions"]
        print(f"{user} - {total_contributions}")
    # print(json.dumps(repo_data, indent=4))
    # stars = repo_data["stargazers_count"]
    # forks = repo_data["forks_count"]
    # open_issues = repo_data["open_issues"]

    # print(f"Stats for {owner}/{repo}")
    # print(f"    Stars - {stars}")
    # print(f"    Forks - {forks}")
    # print(f"    Open Issues - {open_issues}")

    return repo_data

if __name__ == "__main__":
    for key in repos:
        get_repo(key, repos[key])