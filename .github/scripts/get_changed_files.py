import sys
import os

import requests
import openai


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

    prompt = generate_prompt(content)

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    comments = response.choices[0].text
    print(f"AI Code Review Comments: {comments}")

    # posting comments to github PR
    request_body = {
        "body": comments,
        "commit_id": commit_id,
        "path": filename,
        "start_line":1, "start_side": "RIGHT", "line":2, "side": "RIGHT"
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
    print("Github comment response: %s" % response)



def generate_prompt(content):
    raw_code = ''.join(content)

    simple_prompt = "do code review for the Go code below:\n\n" + raw_code
    return simple_prompt


def init_openai():
    openai_org = os.getenv("OPENAI_ORG")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    openai.api_key = openai_api_key



if __name__ == "__main__":
    n = len(sys.argv)
    if n != 4:
        raise Exception("wrong input argument")

    repo_name, pr_number, commit_id = sys.argv[1], sys.argv[2], sys.argv[3]
    print("Path to PR is %s/pulls/%s" % (repo_name, pr_number))

    github_api_key = os.getenv("GITHUB_API_KEY")
    changed_files = get_changed_files_in_pr(repo_name, pr_number, github_api_key)
    print(changed_files)

    init_openai()
    code_review(changed_files, repo_name, pr_number, github_api_key, commit_id)
