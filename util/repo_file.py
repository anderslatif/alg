# this works similarly to repo_path in that it finds the path to the .git directory
# but it creates dirname(*path) if absent
# -------
# For example, repo_file(r, \"refs\" \"remotes\", \"origin\", \"HEAD\") will create
# .git/refs/remotes/origin."""
from util.repo_dir import repo_dir
from util.repo_path import repo_path

def repo_file(repo, *path, mkdir=False):
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)