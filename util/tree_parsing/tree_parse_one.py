from objects.GitTreeLeaf import GitTreeLeaf


def tree_parse_one(raw, start=0):
    # Find the space terminator of the mode
    x = raw.find(b' ', start)
    assert(x-start == 5 or x-start==6)

    # Read the mode
    mode = raw[start:x]

    # Find the NULL terminator of the path
    y = raw.find(b'\x00', x)
    # read the path
    path = raw[x+1:y]

    # Read the SHA and convert to a hex string
    sha = hex(int.from_bytes(raw[y+1:y+21], "big"))[2:] # remove the 0x that hex adds
    return y+21, GitTreeLeaf(mode, path, sha)
