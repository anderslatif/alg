import collections


def commit_or_tag_parser(raw, start=0, dictionary=None):
    if not dictionary:
        # This is set to None as a parameter to avoid recursive calls
        dictionary = collections.OrderedDict()


    space = raw.find(b' ', start)
    newline = raw.find(b'\n', start)

    # Base case
    if (space < 0) or (newline < space):
        # If a newline without a space appears
        # Then it's a blank line and the remainder is the message
        assert(newline == start)
        dictionary[b''] = raw[start+1:]
        return dictionary

    # Recursive case
    # read a key value pair and recurse for the next
    key = raw[start:space]

    # Find the end of the value
    end = start
    # Loop until a space is found
    while True:
        end = raw.find(b'\n', end+1)
        if raw[end+1] != ord(' '): break

    value = raw[space+1:end].replace(b'\n ', b'\n')

    #
    if key in dictionary:
        if type(dictionary[key]) == list:
            dictionary[key].append(value)
        else:
            dictionary[key] = [dictionary[key], value]

    else:
        dictionary[key] = value

    return commit_or_tag_parser(raw, start=end+1, dictionary=dictionary)