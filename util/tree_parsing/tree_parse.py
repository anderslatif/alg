from util.tree_parsing.tree_parse_one import tree_parse_one


def tree_parse(raw):
    pos = 0
    max = len(raw)
    result = list()
    while pos < max:
        pos, data = tree_parse_one(raw, pos)
        result.append(data)

    return result