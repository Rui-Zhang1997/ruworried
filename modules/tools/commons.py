def flatten(lst):
    flat = []
    for i in lst:
        if isinstance(i, list):
            flat += flatten(i)
        else:
            flat.append(i)
    return flat

def reduce(lmda, lst, acc=None):
    s = 0
    if not default:
        s += 1
        acc = lst[0]
    for i in range(s, len(lst)):
        acc = lmda(acc, lst[i])
    return acc
