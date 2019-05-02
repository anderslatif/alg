# https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
class GitIndexEntry(object):
    # The last time a file's metadata changed. This is a tuple (seconds, nanoseconds)
    ctime = None

    # The last time a file's data changed. This is a tuple (seconds, nanoseconds)
    mtime = None

    # the ID of device containing this file
    dev = None

    # The file's inode number
    ino = None

    # The object type, either b1000 (regular), b1010 (symlink), b1110 (gitlink)
    mode_type = None

    # The object permissions as an integer
    mode_permissions = None

    # User ID of owner
    uui = None

    # Group ID of owner
    gid = None

    # Size of this object in bytes
    size = None

    # The object's hash as a hex string
    object = None

    flag_assume_valid = None

    flag_extended = None

    flag_stage = None

    # Length of the name if < OxFFF, -1 otherwise
    flag_name_length = None

    name = None
