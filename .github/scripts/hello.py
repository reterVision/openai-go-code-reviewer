import sys
import os

import requests


def get_changed_files_in_pr(repo_name, pr_number, github_api_key):
    print("Loading files included in PR %s" % pr_number)

    endpoint = "https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"

    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {github_api_key}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json"
        },
    )

    res = response.json()
    for r in res:
        print(r["filename"])


if __name__ == "__main__":
    n = len(sys.argv)
    if n != 3:
        raise Exception("wrong input argument")

    repo_name, pr_number = sys.argv[1], sys.argv[2]
    print("Path to PR is %s/pulls/%s" % (repo_name, pr_number))

    github_api_key = os.getenv("GITHUB_API_KEY")
    changed_files = get_changed_files_in_pr(repo_name, pr_number, github_api_key)
