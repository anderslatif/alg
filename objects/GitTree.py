from objects.git_objects.GitObject import GitObject
from util.tree_parsing.tree_parse import tree_parse
from util.tree_parsing.tree_serialize import tree_serialize


class GitTree(GitObject):
    format = b'tree'

    def deserialize(self, data):
        self.items = tree_parse(data)

    def serialize(self):
        return tree_serialize(self)
