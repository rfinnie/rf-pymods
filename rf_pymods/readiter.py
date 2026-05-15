# SPDX-PackageName: rf-pymods
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://forge.colobox.com/rfinnie/rf-pymods
# SPDX-FileCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT

import itertools


# SPDX-SnippetBegin
# SPDX-SnippetName: readiter from rf-pymods
# SPDX-SnippetComment: Revision 2026-05-14
# SPDX-SnippetComment: Originally from https://forge.colobox.com/rfinnie/rf-pymods
# SPDX-SnippetCopyrightText: © 2020 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT
def readiter(fh, size=1024):
    """Iterate over a filehandle read()"""
    return itertools.takewhile(lambda t: t, map(lambda chunk: fh.read(size), itertools.count(0)))


# SPDX-SnippetEnd
