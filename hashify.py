
def hashify(o):
    """returns a hashable value. Use unhashify() to invert."""
    if type(o) == list:
        return (list,)+tuple(map(hashify,o))
    elif type(o) == set:
        return (set,)+tuple(sorted(o))
    elif type(o) == dict:
        return (dict,)+tuple(sorted((k,hashify(o[k])) for k in o))
    elif type(o) == tuple:
        return (tuple,)+tuple(map(hashify,o))
    else:
        return o

def unhashify(o):
    if type(o) == tuple:
        datatype, rest = o[0], o[1:]
        if datatype == dict:
            info = map(lambda (k,v): (k,unhashify(v)), rest)
        elif datatype == set:
            info = rest
        else:
            info = map(unhashify, rest)
        return datatype(info)
    else:
        return o

# make a super complicated object:
#
# O = {(1,2,3):[1,2,[3]], "hello":{3:4,"a":[4,"b"]}, 1.01:{10,11,12,(13,12),14}}
#
# ordinarily we couldn't hash this, but:
#
# H = hashify(O)
# mySet = {1,2,3,H}
# myDict = {1:H, H:1}
# print hash(H)
#
# and it's invertible:
#
# assert(unhashify(H) == O)
