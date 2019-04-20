import os

# find the path to the .git directory
def repo_path(repo, *path):
    return os.path.join(repo.gitdir, *path)