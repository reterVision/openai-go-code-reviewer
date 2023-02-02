import sys
import os

n = len(sys.argv)
print("Total arguments passed:", n)

if n != 3:
    raise Exception("wrong input argument")

repo_name, pr_number = sys.argv[1], sys.argv[2]

print("Path to PR is %s/pulls/%s" % (repo_name, pr_number))
