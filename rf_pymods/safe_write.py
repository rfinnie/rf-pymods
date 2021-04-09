# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import os
import uuid


def safe_write(file, **kwargs):
    """(Try to) safely write files with minimum collision possibility"""
    # SPDX-SnippetComment: Originally from https://github.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
    # SPDX-LicenseInfoInSnippet: MIT

    def _sw_close(fh):
        if fh.closed:
            return
        fh._fh_close()
        os.rename(fh.name, fh.original_name)

    if "mode" not in kwargs:
        kwargs["mode"] = "x"
    temp_name = "{}.tmp{}~".format(file, str(uuid.uuid4()))
    fh = open(temp_name, **kwargs)
    setattr(fh, "original_name", file)
    setattr(fh, "_fh_close", fh.close)
    setattr(fh, "close", lambda: _sw_close(fh))
    return fh
