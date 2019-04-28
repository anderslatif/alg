import collections
import os

from util.ref_handling.ref_resolver import ref_resolver
from util.repo_handling.repo_dir import repo_dir


def ref_lister(repo, path=None):
    if not path:
        path = repo_dir(repo, "refs")
        result = collections.OrderedDict()
    # Sort the output of listdir cause Git does as well
    for file in sorted(os.listdir(path)):
        path = os.path.join(path, file)
        if os.path.isdir(path):
            result[file] = ref_lister(repo, path)
        else:
            result[file] = ref_resolver(repo, path)

    return result
