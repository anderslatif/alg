# To access the commandline args
import sys
# https://docs.python.org/3/library/argparse.html
import argparse
# Git uses a configuration file format that is basically Microsoft’s INI format. The configparser module can read and write these files.
# import configparser
# need to use the SHA-1 function for hashing
# filesystem abstractions
# regular expressions
# zip functionality

# object imports
from objects.GitRepository import GitRepository

# util helper function imports
from objects.git_objects.GitBlob import GitBlob
from objects.git_objects.GitCommit import GitCommit
from util.object_handling.object_find import object_find
from util.object_handling.object_read import object_read
from util.object_handling.object_write import object_write
from util.repo_handling.repo_create import repo_create
from util.repo_handling.repo_find import repo_find

argparser = argparse.ArgumentParser(description="Anders Latif's own git implementation")

argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add":
        cmd_add(args)
    elif args.command == "cat-file"    : cmd_cat_file(args)
    # elif args.command == "checkout"    : cmd_checkout(args)
    # elif args.command == "commit"      : cmd_commit(args)
    elif args.command == "hash-object" : cmd_hash_object(args)
    elif args.command == "init"        : cmd_init(args)
    elif args.command == "log"         : cmd_log(args)
    elif args.command == "ls-tree"     : cmd_ls_tree(args)
    # elif args.command == "merge"       : cmd_merge(args)
    # elif args.command == "rebase"      : cmd_rebase(args)
    # elif args.command == "rev-parse"   : cmd_rev_parse(args)
    # elif args.command == "rm"          : cmd_rm(args)
    # elif args.command == "show-ref"    : cmd_show_ref(args)
    # elif args.command == "tag"         : cmd_tag(args)


# ----------------------------------- INIT -----------------------------------
argsparsed = argsubparsers.add_parser("init", help="Initializea a new, empty repository")

argsparsed.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repistory")


def cmd_init(args):
    repo_create(args.path)


def cmd_add(args):
    pass


# ---------------------------------- CAT FILE ----------------------------------
argsparsed = argsubparsers.add_parser("cat-file", help="Provide content of repository object")

argsparsed.add_argument("type", metavar="type", choices=["blob", "commit", "tag", "tree"], help="Specify the type")

argsparsed.add_argument("object", metavar="object", help="The object type to display")

def cmd_cat_file(args):
    repo = repo_find()
    cat_file(repo, args.object, format=args.type.encode())

def cat_file(repo, obj, format=None):
    obj = object_read(repo, object_find(repo, obj, format=format))
    sys.stdout.buffer.write(obj.serialize())


# --------------------------------- HASH-OBJECT --------------------------------
argsparsed = argsubparsers.add_parser("hash-object", help="Compute object ID and optionally creates a blob from a file")

argsparsed.add_argument("-t", metavar="type", dest="type", choices=["blob", "commit", "tag", "tree"])

argsparsed.add_argument("-w", dest="write", action="store_true", help="Actually write the object into the database")

argsparsed.add_argument("path", help="Read object from <file>")

def cmd_hash_object(args):
    if args.write:
        repo = GitRepository(".")
    else:
        repo = None

    with open(args.path, "rb") as fileDestination:
        sha = object_hash(fileDestination, args.type.encode(), repo)
        print(sha)

def object_hash(fileDestination, format, repo=None):
    data = fileDestination.read()

    # Choosing constructor depending on object type found in header
    if   format==b'commit' : obj = GitCommit(repo, data)
    elif format==b'tree'   : obj = GitTree(repo, data)
    elif format==b'tag'    : obj = GitTag(repo, data)
    elif format==b'blob'    : obj = GitBlob(repo, data)
    else:
        raise Exception("Unknown type %s" % format)

    return object_write(obj, repo)

# -------------------------------------- LOG -------------------------------------
argsparsed = argsubparsers.add_parser("log", help="Display history of a given commit")
argsparsed.add_argument("commit", default="HEAD", nargs="?", help="Commit to start at")

def cmd_log(args):
    repo = repo_find()

    print("diagraph alglog{")
    log_graphviz(repo, object_find(repo, args.commit), set())
    print("}")

def log_graphviz(repo, sha, seen):
    if sha in seen:
        return
    seen.add(sha)

    commit = object_read(repo, sha)
    assert (commit.format==b'commit')

    if not b'parent' in commit.commit_or_tag.keys():
        # Initial commit
        return

    parents = commit.commit_or_tag[b'parent']

    if type(parents) != list:
        parents = [parents]

    for parent in parents:
        parent = parent.decode("ascii")
        print ("c_{0} -> c_{1};".format(sha, parent))
        log_graphviz(repo, parent, seen)

# ------------------------------------ LS-TREE -----------------------------------

argsparsed = argsubparsers.add_parser("ls-tree", help="Pretty-print a tree object")
argsparsed.add_argument("object", help="The object to show")

def cmd_ls_tree(args):
    repo = repo_find()
    object = object_read(repo, object_find(repo, args.object, format=b'tree'))

    for item in object.items:
        print("{0} {1} {2}\t{3}".format(
            "0" * (6 - len(item.mode)) + item.mode.decode("ascii"),
            # Git's ls-tree displays the type of the object pointed to
            object_read(repo, item.sha).fmt.decode("ascii"),
            item.sha,
            item.path.decode("ascii")
        ))