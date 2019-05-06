# Same as repo_handling-path but mkdir *path wil be absent if mkdir is "" (empty)
import os

from util.repo_handling.repo_path import repo_path


def repo_dir(repo, *path, mkdir=False):
    path = repo_path(repo, *path)

    if os.path.exists(path):
        if (os.path.isdir(path)):
            return path
        else:
            raise Exception("Not a directory %s" % path)

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None
