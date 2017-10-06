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

def categorize(lst, *args):
    a = [[] for i in range(len(args))]
    rem = []
    for l in lst:
        no_match = True
        for i in range(len(args)):
            fn = args[i]
            if fn(l):
                a[i].append(l)
                no_match = False
                continue
        if no_match:
            rem.append(l)
    return (a, rem)
