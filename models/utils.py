import os
import copy
import shutil


def clean_dir(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise IOError("no such directory: '{}'".format(path))
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


def copy_tree(src, dst, symlinks=False):
    try:
        if not os.path.exists(dst):
            os.mkdir(dst)

    except OSError as exc:
        if '[Errno 22] Invalid argument' in str(exc):
            return False
        else:
            raise

    else:
        for name in os.listdir(src):
            src_path = os.path.join(src, name)
            dst_path = os.path.join(dst, name)

            if os.path.isdir(src_path):
                copy_tree(src_path, dst_path, symlinks=symlinks)
            elif os.path.isfile(src_path):
                copy_file(src_path, dst_path)
            elif os.path.islink(src_path) and symlinks:
                copy_link(src_path, dst_path)

        return True


def copy_file(src, dst):
    try:
        shutil.copyfile(src, dst)
        return True
    except OSError as exc:
        if '[Errno 22] Invalid argument' in str(exc):
            return False
        else:
            raise


def copy_link(src, dst):
    linkto = os.readlink(src)
    os.symlink(linkto, dst)
