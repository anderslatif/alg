class GitObject(object):
    repo = None

    def __init__(self, repo, data=None):
        self.repo = repo

        if data != None:
            self.deserialize(data)

    def serialize(self):
        # this function must be implemented by the subclasses
        raise Exception("Unimplemented!")

    def deserialize(self, data):
        raise Exception("Unimplemented.")
