def commit_or_tag_serialize(commit_or_tag):
    result = b''

    # Output fields
    for key in commit_or_tag.keys():
        # Skip the message
        if key == b'': continue
        value = commit_or_tag[key]

        # Normalize to a list
        if type(value) != list:
            value = [value]

        for val in value:
            result += key + b' ' + (val.replace(b'\n', b'\n ')) + b'\n'

        # Append message
        result += b'\n' + commit_or_tag[b'']

        return result;