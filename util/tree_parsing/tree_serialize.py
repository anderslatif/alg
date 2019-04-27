# A tree: [mode] space [path] 0x00 [sha-1]
def tree_serialize(obj):
    result = b''
    for item in obj.items:
        result += item.mode
        result += b' '
        result += item.path
        result += b'\x00'
        sha = int(item.sha, 16)
        result += sha.to_bytes(20, byteorder="big")
    return result
