import sys
import os

import requests


code_review_endpoint = os.getenv("CODE_REVIEW_ENDPOINT")
code_review_api_key = os.getenv("CODE_REVIEW_API_KEY")


def get_changed_files_in_pr(repo_name, pr_number, github_api_key):
    endpoint = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
    print(f"Loading files included in PR {endpoint}")

    response = requests.get(
        endpoint,
        headers={
            "Authorization": f"Bearer {github_api_key}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json"
        },
    )

    res = response.json()

    filenames = []
    for r in res:
        filename = r["filename"]
        if filename[-3:] == ".go":
            filenames.append(filename)
    return filenames


def code_review(filenames, repo_name, pr_number, github_api_key, commit_id):
    for filename in filenames:
        with open(filename) as f:
            content = f.readlines()
        review_contents(filename, content, repo_name, pr_number, github_api_key, commit_id)


def review_contents(filename, content, repo_name, pr_number, github_api_key, commit_id):
    github_comment_endpoint = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/comments"
    print(f"Github commenting URL: {github_comment_endpoint}")


    comments = get_review_comments(content)
    print(f"AI Code Review Comments: {comments}")

    # posting comments to github PR
    request_body = {
        "body": comments,
        "commit_id": commit_id,
        "path": filename,
        "start_line":1, "start_side": "RIGHT", "line":1, "side": "RIGHT"
    }
    print(f"Github request body: {request_body}")

    response = requests.post(
        github_comment_endpoint,
        headers={
            "Authorization": f"Bearer {github_api_key}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json"
        },
        json=request_body
    )
    print("Github comment response: %s" % response.json())


def get_review_comments(content):
    global code_review_endpoint
    global code_review_api_key

    raw_code = ''.join(content)
    request_body = {
        "code": raw_code
    }
    response = requests.post(
        code_review_endpoint,
        headers={
            "X-Api-Key": f"{code_review_api_key}",
            "Content-Type": "application/json; charset=UTF-8"
        },
        json=request_body
    ).json()
    return response["Comments"]



if __name__ == "__main__":
    n = len(sys.argv)
    if n != 4:
        raise Exception("wrong input argument")

    repo_name, pr_number, commit_id = sys.argv[1], sys.argv[2], sys.argv[3]
    print("Path to PR is %s/pulls/%s" % (repo_name, pr_number))

    github_api_key = os.getenv("GITHUB_API_KEY")
    changed_files = get_changed_files_in_pr(repo_name, pr_number, github_api_key)
    print(changed_files)

    code_review(changed_files, repo_name, pr_number, github_api_key, commit_id)
