from objects.git_objects.GitObject import GitObject
from util.commit_handling.commit_or_tag_parser import commit_or_tag_parser
from util.commit_handling.commit_or_tag_serialize import commit_or_tag_serialize


class GitCommit(GitObject):
    format = b'commit'

    def deserialize(self, data):
        self.commit_or_tag = commit_or_tag_parser(data)

    def serialize(self):
        return commit_or_tag_serialize(self.commit_or_tag)