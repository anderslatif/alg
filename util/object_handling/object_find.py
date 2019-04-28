from util.object_handling.object_read import object_read
from util.object_handling.object_resolve import object_resolve


def object_find(repo, name, format=None, follow=True):
    sha = object_resolve(repo, name)

    if not sha:
        raise Exception("No such reference {0}".format(name))

    if len(sha) > 1:
        raise Exception("Ambigous reference {0}: Candidates are:\n - {1}".format(name, "\n - ".join(sha)))

    sha = sha[0]

    if not format:
        return sha

    while True:
        object = object_read(repo, sha)

        if object.format == format:
            return sha

        if not follow:
            return  None

        # Follow tags
        if object.format == b'tag':
            sha = object.commit_or_tag[b'object'].decode("ascii")
        elif object.format == b'commit' and format == b'tree':
            sha = object.commit_or_tag[b'tree'].decode("ascii")
        else:
            return None
