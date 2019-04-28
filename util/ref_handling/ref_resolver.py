from util.repo_handling.repo_file import repo_file


def ref_resolver(repo, ref):
    with open(repo_file(repo, ref), 'r') as fp:
        data = fp.read()[:-1] # drops the final \n
    if data.startswith("ref: "):
        return ref_resolver(repo, data[5:])
    else:
        return data
