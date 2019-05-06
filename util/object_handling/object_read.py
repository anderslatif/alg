# Read object object_id and return a GitObject
import zlib

from objects.GitTag import GitTag
from objects.GitTree import GitTree
from objects.git_objects.GitBlob import GitBlob
from objects.git_objects.GitCommit import GitCommit
from util.repo_handling.repo_file import repo_file


def object_read(repo, sha):
    path = repo_file(repo, "objects", sha[0:2], sha[2:])

    with open(path, "rb") as f:
        raw = zlib.decompress(f.read())

        # Object type
        x = raw.find(b' ')
        format = raw[0:x]

        # Read and validate object size
        y = raw.find(b'\x00', x)
        size = int(raw[x:y].decode("ascii"))
        if size != len(raw)-y-1:
            raise Exception("Malformed object {0}: bad length".format(sha))

        # Pick constructor
        if   format==b'commit' : c=GitCommit
        elif format==b'tree'   : c=GitTree
        elif format==b'tag'    : c=GitTag
        elif format==b'blob'   : c=GitBlob
        else:
            raise Exception("Unknown type %s for object %s".format(format.decode("ascii", sha)))

    return c(repo, raw[y+1:])
