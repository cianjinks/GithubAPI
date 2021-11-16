from github import Github
import os
from pprint import pprint

token = os.getenv('GITHUB_TOKEN', '...')
g = Github(token)
repo = g.get_repo("cianjinks/GithubAPI")
user = g.get_user()
print(user.login)
print(user.name)

clones = repo.get_clones_traffic(per="day")
views = repo.get_views_traffic(per="day")

print(f"Repository has {clones['count']} clones out of which {clones['uniques']} are unique.")
print(f"Repository has {views['count']} views out of which {views['uniques']} are unique.")

best_day = max(*list((day.count, day.timestamp) for day in views["views"]), key=itemgetter(0))

pprint(views)
print(f"Repository had most views on {best_day[1]} with {best_day[0]} views")