import errno
import fcntl
import os
import sys


class runtime_lock:
    """Lock a process to prevent concurrent runtimes

    Usage:
        with runtime_lock():
            pass

    If name is not provided, the script filename is determined.
    If lock_dir is not provided, the most appropriate lock directory is
    determined.
    """

    # SPDX-SnippetComment: Originally from https://github.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
    # SPDX-LicenseInfoInSnippet: MIT

    filename = None
    fh = None

    def __init__(self, name=None, lock_dir=None):
        if name is None:
            if sys.argv[0]:
                name = os.path.basename(sys.argv[0])
            else:
                name = os.path.basename(__file__)
        if lock_dir is None:
            for dir in ("/run/lock", "/var/lock", "/run", "/var/run", "/tmp"):
                if os.path.exists(dir):
                    lock_dir = dir
                    break
            if lock_dir is None:
                raise FileNotFoundError("Suitable lock directory not found")
        filename = os.path.join(lock_dir, "{}.lock".format(name))

        # Do not set fh to self.fh until lockf/flush/etc all succeed
        fh = open(filename, "w")
        try:
            fcntl.lockf(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError as e:
            if e.errno in (errno.EACCES, errno.EAGAIN):
                raise
        fh.write("%10s\n" % os.getpid())
        fh.flush()
        fh.seek(0)

        self.fh = fh
        self.filename = filename

    def close(self):
        if self.fh:
            self.fh.close()
            self.fh = None
            os.unlink(self.filename)

    def __del__(self):
        self.close()

    def __enter__(self):
        self.fh.__enter__()
        return self

    def __exit__(self, exc, value, tb):
        result = self.fh.__exit__(exc, value, tb)
        self.close()
        return result
