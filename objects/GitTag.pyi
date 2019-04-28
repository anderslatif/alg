from objects.git_objects.GitCommit import GitCommit


class GitTag(GitCommit):
    format = b'tag'
