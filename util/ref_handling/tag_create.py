import collections

from objects.GitRepository import GitRepository
from objects.GitTag import GitTag
from util.object_handling.object_find import object_find
from util.object_handling.object_write import object_write


def tag_create(repo: GitRepository, name, reference, author, create_tag_object):
    sha = object_find(repo, reference)


    if create_tag_object:
        # create tag object commit
        tag = GitTag(repo)
        tag.commit_or_tag = collections.OrderedDict()
        tag.commit_or_tag[b'object'] = sha.encode()
        tag.commit_or_tag[b'type'] = b'commit'
        tag.commit_or_tag[b'tag'] = name.encode()
        tag.commit_or_tag[b'tagger'] = bytes(author.encode())
        tag.commit_or_tag[b''] = b'This is the commit message that should have come from the user\n'
        tag_sha = object_write(tag, repo)
        ref_create(repo, "tags/" + name, tag_sha)
    else:
        # create lightweight tag (ref)
        ref_create(repo, "tags/", name, sha)