import os
import copy


def clean_dir(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise IOError("no such directory: '{}'".forder(path))
    if not os.path.isdir(path):
        raise IOError("'{}' is not a directory".format(path))
    return path


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def unordered_lists_equal(lst1, lst2, cmp_func=None):
    if cmp_func is None:
        cmp_func = lambda a, b: a == b

    if len(lst1) == len(lst2):
        lst1_copy = copy.copy(lst1)
        lst2_copy = copy.copy(lst2)
        while lst1_copy and lst2_copy:
            index = None
            for i, e in enumerate(lst2_copy):
                if cmp_func(lst1_copy[0], e):
                    index = i
                    break
            if index is not None:
                del lst1_copy[0]
                del lst2_copy[index]
            else:
                return False
        return True

    return False
