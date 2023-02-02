import os

repo_name = os.getenv("GIT_REPO")
pr_number = os.getenv("PR_NUMBER")

print("Path to PR is %s/pulls/%s" % (repo_name, pr_number))
