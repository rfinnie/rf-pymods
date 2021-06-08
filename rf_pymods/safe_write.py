# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import os
import shutil
import uuid


def safe_write(file, **kwargs):
    """(Try to) safely write files with minimum collision possibility

    The returned filehandle object performs identically to a real open()
    filehandle, but is writing to a temporary file in the same
    directory, and will move the file into place after filehandle
    close or __exit__.

    By default, the temporary file is opened "x", which will resist
    filename guessing collisions and should raise FileExistsError if
    such a collision can occur.

    By default, if the file exists beforehand, file stats will attempt
    to be copied to the temporary file upon open, which in turn will be
    moved to the final file upon close.  Use preserve_stats=False to
    disable this behavior.  You may also change stats while the
    filehandle is open and they will be preserved upon close:

        with safe_write("foo") as f:
            os.fchmod(f.fileno(), 0o0600)
            os.fchown(f.fileno(), 1000, 1000)
    """
    # SPDX-SnippetComment: Originally from https://github.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
    # SPDX-LicenseInfoInSnippet: MIT

    def _sw_close(fh):
        if fh.closed:
            return
        fh._fh_close()
        os.rename(fh.name, fh.dest_name)
        setattr(fh, "name", fh.dest_name)

    preserve_stats = True
    if "preserve_stats" in kwargs:
        preserve_stats = bool(kwargs["preserve_stats"])
        del kwargs["preserve_stats"]
    if "mode" not in kwargs:
        kwargs["mode"] = "x"
    temp_name = "{}.tmp{}~".format(file, str(uuid.uuid4()))
    fh = open(temp_name, **kwargs)
    if preserve_stats and os.path.exists(file):
        shutil.copystat(file, temp_name)
    setattr(fh, "dest_name", file)
    setattr(fh, "_fh_close", fh.close)
    setattr(fh, "close", lambda: _sw_close(fh))
    return fh
