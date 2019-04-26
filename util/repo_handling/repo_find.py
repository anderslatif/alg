import os

from objects.GitRepository import GitRepository

# helps in finding the path to the repository root
# this is because it is possible to call alg within subdirectories as well


def repo_find(path=".", required=True):
    path = os.path.realpath(path)

    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepository(path)

    # if we don't have the .git directory then recursively go through parents
    parent = os.path.realpath(os.path.join(path, ".."))

    if parent == path:
        if required:
            raise Exception("No git directory")
        else:
            return None
    return repo_find(parent, required)
