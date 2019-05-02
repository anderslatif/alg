import os
import sys
# https://docs.python.org/3/library/argparse.html
import argparse
# Git uses a configuration file format that is basically Microsoft’s INI format. The configparser module can read and write these files.

# object imports
from objects.GitRepository import GitRepository
from objects.GitTag import GitTag

from objects.GitTree import GitTree
from objects.git_objects.GitBlob import GitBlob
from objects.git_objects.GitCommit import GitCommit

# util helper function imports
from util.ref_handling.tag_create import tag_create
from util.commit_handling.tree_checkout import tree_checkout
from util.object_handling.object_find import object_find
from util.object_handling.object_read import object_read
from util.object_handling.object_write import object_write
from util.ref_handling.ref_lister import ref_lister
from util.repo_handling.repo_create import repo_create
from util.repo_handling.repo_find import repo_find

argparser = argparse.ArgumentParser(description="ALG: Anders Latif's own git implementation")

argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add":
        cmd_add(args)
    elif args.command == "cat-file"    : cmd_cat_file(args)
    elif args.command == "checkout"    : cmd_checkout(args)
    # elif args.command == "commit"      : cmd_commit(args)
    elif args.command == "hash-object" : cmd_hash_object(args)
    elif args.command == "init"        : cmd_init(args)
    elif args.command == "log"         : cmd_log(args)
    elif args.command == "ls-tree"     : cmd_ls_tree(args)
    # elif args.command == "merge"       : cmd_merge(args)
    # elif args.command == "rebase"      : cmd_rebase(args)
    elif args.command == "rev-parse"   : cmd_rev_parse(args)
    # elif args.command == "rm"          : cmd_rm(args)
    elif args.command == "show-ref"    : cmd_show_ref(args)
    elif args.command == "tag"         : cmd_tag(args)


# ----------------------------------- INIT -----------------------------------
parser = argsubparsers.add_parser("init", help="Initializea a new, empty repository")

parser.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repistory")


def cmd_init(args):
    repo_create(args.path)


def cmd_add(args):
    pass


# ---------------------------------- CAT FILE ----------------------------------
parser = argsubparsers.add_parser("cat-file", help="Provide content of repository object")

parser.add_argument("type", metavar="type", choices=["blob", "commit", "tag", "tree"], help="Specify the type")

parser.add_argument("object", metavar="object", help="The object type to display")


def cmd_cat_file(args):
    repo = repo_find()
    cat_file(repo, args.object, format=args.type.encode())


def cat_file(repo, obj, format=None):
    obj = object_read(repo, object_find(repo, obj, format=format))
    sys.stdout.buffer.write(obj.serialize())


# --------------------------------- HASH-OBJECT --------------------------------
parser = argsubparsers.add_parser("hash-object", help="Compute object ID and optionally creates a blob from a file")

parser.add_argument("-t", metavar="type", dest="type", choices=["blob", "commit", "tag", "tree"])

parser.add_argument("-w", dest="write", action="store_true", help="Actually write the object into the database")

parser.add_argument("path", help="Read object from <file>")


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
parser = argsubparsers.add_parser("log", help="Display history of a given commit")
parser.add_argument("commit", default="HEAD", nargs="?", help="Commit to start at")


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

parser = argsubparsers.add_parser("ls-tree", help="Pretty-print a tree object")
parser.add_argument("object", help="The object to show")


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

# ------------------------------------ CHECKOUT -----------------------------------

parser = argsubparsers.add_parser("checkout", help="checkout a commit inside of a directory")

parser.add_argument("commit", help="The commit or tree to checkout")

parser.add_argument("path", help="The EMPTY directory to checkout on")


def cmd_checkout(args):
    repo = repo_find()

    object = object_read(repo, object_find(repo, args.commit))

    # If the object is a commit, then grab its tree
    if object.fmt == b'commit':
        object = object_read(repo, object.commit_or_parse[b'tree'].decode("ascii"))

        # Verify that the path is an empty directory
        if os.path.exists(args.path):
            if not os.path.isdir(args.path):
                raise Exception("Not a directory {0}!".format(args.path))
            if os.listdir(args.path):
                raise Exception("Not empty {0}!".format(args.path))
    else:
        os.makedirs(args.path)

    tree_checkout(repo, object, os.path.realpath(args.path).encode())

# ------------------------------------ SHOW-REFS ----------------------------------

parser = argsubparsers.add_parser("show-ref", help="List references")


def cmd_show_ref(args):
    repo = repo_find()
    refs = ref_lister(repo)
    show_ref(repo, refs, prefix="refs")


def show_ref(repo, refs, with_hash=True, prefix=""):
    for key, value in refs.items():
        if type(value) == str:
            print("{0}{1}{2}".format(
                value + " " if with_hash else "",
                prefix + "/" if prefix else "",
                key
            ))
        else:
            show_ref(repo, value, with_hash=with_hash, prefix="{0}{1}{2}".format(
                                                                                prefix,
                                                                                "/" if prefix else "",
                                                                                key
                                                                            ))
# ---------------------------------------- TAG --------------------------------------

# git tag                   - Lists all
# git tag NAME [OBJECT]     - Create a lightweight tag
# git tag -a NAME [OBJECT]  - Create an object tag

parser = argsubparsers.add_parser("tag", help="List and create tags")

parser.add_argument("-a", action="store_true", dest="create_tag_object", help="Creates a tag object")

parser.add_argument("name", nargs="?", help="The new tag's name")

parser.add_argument("object", default="HEAD", nargs="?", help="The object the new tag will point to")

# todo change the default, consider if I want to parse from git config --list
parser.add_argument("author", default="Anders Latif <anderslatif@gmail.com>", nargs="?", help="Author of the commit or tag")


def cmd_tag(args):
    repo = repo_find()

    if args.name:
        tag_create(name=args.name, reference=args.object, author=args.author, create_tag_object=args.create_tag_object)
    else:
        refs = ref_lister(repo)
        show_ref(repo, refs["tags"], with_hash=False)

# ---------------------------------------- REV-PARSE --------------------------------------

parser = argsubparsers.add_parser("rev-parse", help="Parse revision (or other objects) identifiers")

parser.add_argument("--alg-type", metavar="type", dest="type", choices=["blob", "commit", "tag", "tree"],
                        default=None, help="Specify the expected type")

parser.add_argument("name", help="The name to parse")


def cmd_rev_parse(args):
    if args.type:
        format = args.type.encode()

    repo = repo_find()

    print (object_find(repo, args.name, args.type, follow=True))


