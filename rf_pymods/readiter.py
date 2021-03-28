# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import itertools


def readiter(fh, size=1024):
    """Iterate over a filehandle read()"""
    # SPDX-SnippetComment: Originally from https://github.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
    # SPDX-LicenseInfoInSnippet: MIT

    return itertools.takewhile(
        lambda t: t, map(lambda chunk: fh.read(size), itertools.count(0))
    )
