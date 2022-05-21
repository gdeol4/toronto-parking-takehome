# this function comes from the flatten-json library
def flatten_json(nested_json: dict, exclude: list=['']) -> dict:
    """
    Flatten a list of nested dicts.
    """
    out = dict()
    def flatten(x: (list, dict, str), name: str='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude:
                    flatten(x[a], f'{name}{a}_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, f'{name}{i}_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out