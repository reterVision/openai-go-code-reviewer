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
        additions = r["additions"]
        if filename[-3:] != ".go" or additions <= 0:
            continue

        patch = r["patch"].split('\n')
        print(patch)

        code_blocks = []
        single_block = []

        # Separating modified blocks for independent reviews
        for line in patch:
            if len(line) > 0 and line[0] == "+":
                single_block.append(line[1:] + '\n')
                continue
            if len(single_block) > 0:
                code_blocks.append(single_block)
                single_block = []

        if len(single_block) > 0:
            code_blocks.append(single_block)
            single_block = []

        filenames.append((filename, code_blocks))

    return filenames


def code_review(content, repo_name, pr_number, github_api_key, commit_id):
    for content in content:
        filename, code_blocks = content[0], content[1]

        with open(filename) as f:
            raw_file = f.readlines()

        for code_block in code_blocks:
            if len(code_block) == 0:
                continue

            first_line = code_block[0]
            for line_number, line in enumerate(raw_file):
                if line == first_line:
                    break

            print((first_line, line_number+1))
            review_contents(filename, line_number, code_block, repo_name, pr_number, github_api_key, commit_id)


def review_contents(filename, line_number, content, repo_name, pr_number, github_api_key, commit_id):
    comments = get_review_comments(content)
    print(f"AI Code Review Comments: {comments}")

    github_comment_endpoint = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/comments"
    print(f"Github commenting URL: {github_comment_endpoint}")

    # posting comments to github PR
    request_body = {
        "body": comments,
        "commit_id": commit_id,
        "path": filename,
        "start_line":line_number, "start_side": "RIGHT", "line":line_number+1, "side": "RIGHT"
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
