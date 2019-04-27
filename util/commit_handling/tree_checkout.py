import os

from util.object_handling.object_read import object_read


def tree_checkout(repo, tree, path):
    for item in tree.items:
        object = object_read(repo, item.sha)
        destination = os.path.join(path, item.path)

        if object.fmt == b'tree':
            os.mkdir(destination)
            tree_checkout(repo, object, destination)
        elif object.fmt == b'blob':
            with open(destination, 'wb') as f:
                f.write(object.blobdata)
