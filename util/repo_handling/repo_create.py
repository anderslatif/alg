# Instantiating a new GitRepository object at path
# conditional based on if directory already exists
import os

from objects.GitRepository import GitRepository
from util.repo_handling.repo_default_config import repo_default_config
from util.repo_handling.repo_dir import repo_dir
from util.repo_handling.repo_file import repo_file


def repo_create(path):
    repo = GitRepository(path, True)

    # does path exist?
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception ("%s is not a directory!" % path)
        # is not empty?
        if os.listdir(repo.worktree):
            raise Exception("%s is not empty!" % path)

    else:
        os.makedirs(repo.worktree)

    assert(repo_dir(repo, "branches", mkdir=True))
    assert(repo_dir(repo, "objects", mkdir=True))
    assert(repo_dir(repo, "refs", "tags", mkdir=True))
    assert(repo_dir(repo, "refs", "heads", mkdir=True))

    # .git/description
    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # .git/HEAD
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo
