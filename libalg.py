# To access the commandline args
import sys
# https://docs.python.org/3/library/argparse.html
import argparse
import collections
# Git uses a configuration file format that is basically Microsoft’s INI format. The configparser module can read and write these files.
# import configparser
# need to use the SHA-1 function for hashing
import hashlib
# filesystem abstractions
import os
# regular expressions
import re
# zip functionality
import zlib

# util helper function imports
from util.repo_create import repo_create

argparser = argparse.ArgumentParser(description="Anders Latif's own git implementation")

argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add":
        cmd_add(args)
    # elif args.command == "cat-file"    : cmd_cat_file(args)
    # elif args.command == "checkout"    : cmd_checkout(args)
    # elif args.command == "commit"      : cmd_commit(args)
    # elif args.command == "hash-object" : cmd_hash_object(args)
    elif args.command == "init"        : cmd_init(args)
    # elif args.command == "log"         : cmd_log(args)
    # elif args.command == "ls-tree"     : cmd_ls_tree(args)
    # elif args.command == "merge"       : cmd_merge(args)
    # elif args.command == "rebase"      : cmd_rebase(args)
    # elif args.command == "rev-parse"   : cmd_rev_parse(args)
    # elif args.command == "rm"          : cmd_rm(args)
    # elif args.command == "show-ref"    : cmd_show_ref(args)
    # elif args.command == "tag"         : cmd_tag(args)


from objects.GitRepository import GitRepository

argsp = argsubparsers.add_parser("init", help="Initializea a new, empty repository")

argsp.add_argument("path", metavar="directory", nargs="?", default=".", help="Where to create the repistory")


def cmd_init(args):
    repo_create(args.path)


def cmd_add(args):
    pass
