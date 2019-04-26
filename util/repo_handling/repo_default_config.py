import configparser


def repo_default_config():
    config = configparser.ConfigParser()

    config.add_section("core")
    # repositoryformatversion = 0: the version of the gitdir format.
    # 0 means the initial format, 1 the same with extensions.
    # alg only accepts 0
    config.set("core", "repoistoryformatversion", "0")
    # filemode = false: disable tracking of file mode changes in the work tree.
    config.set("core", "filemode", "false")
    # bare = false: indicates that this repository has a worktree.
    # Git supports an optional worktree key which indicates the location of the worktree, if not - alg doesn’t.
    config.set("core", "bare", "false")

    return config
