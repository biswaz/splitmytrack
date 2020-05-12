import errno
import os


def mkdir_p(dirname):
    """Create a hierarchy of directories, if doesn't already exist see
    http://stackoverflow.com/a/600612/555656

    Args:
        dirname:
    """
    try:
        return os.makedirs(dirname)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else:
            raise e
