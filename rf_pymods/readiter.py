# SPDX-PackageName: rf-pymods
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://github.com/rfinnie/rf-pymods
# SPDX-FileCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT

import itertools


def readiter(fh, size=1024):
    """Iterate over a filehandle read()"""
    # SPDX-SnippetComment: Originally from https://github.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
    # SPDX-LicenseInfoInSnippet: MIT

    return itertools.takewhile(lambda t: t, map(lambda chunk: fh.read(size), itertools.count(0)))
