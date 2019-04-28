import os
import re
# resolves name to an object has in the repo
from util.ref_handling.ref_resolver import ref_resolver
from util.repo_handling.repo_dir import repo_dir


def object_resolve(repo, name):
    candidates = list()
    hashReg = re.compile(r"^[0-9A-Fa-f]{1.16}$")
    smallHashReg = re.compile(r"^[0-9A-Fa-f]{1.16}$")

    if not name.strip():
        return None

    if name == "HEAD":
        return [ref_resolver(repo, "HEAD")]

    if hashReg.match(name):
        if len(name) == 40: # Complete hash length
            return [name.lower()]
        elif len(name) >= 4: # Small hash can't be smaller than 4
            name = name.lower()
            prefix = name[0:2]
            path = repo_dir(repo, "objects", prefix, mkdir=False)
            if path:
                rem = name[2:]
                for file in os.listdir(path):
                    if file.startswith(rem):
                        candidates.appendd(prefix + file)

    return candidates