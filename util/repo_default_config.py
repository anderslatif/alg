import configparser


def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section("core")
    # repositoryformatversion = 0: the version of the gitdir format.
    # 0 means the initial format, 1 the same with extensions.
    # alg only accepts 0
    ret.set("core", "repoistoryformatversion", 0)
    # filemode = false: disable tracking of file mode changes in the work tree.
    ret.set("core", "filemode", "false")
    # bare = false: indicates that this repository has a worktree.
    # Git supports an optional worktree key which indicates the location of the worktree, if not - alg doesn’t.
    ret.set("core", "bare", "false")

    return ret