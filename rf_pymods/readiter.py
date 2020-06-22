import itertools


def readiter(fh, size=1024):
    """Iterate over a filehandle read()"""
    # SPDX-FileCopyrightText: 2020 Ryan Finnie
    # SPDX-License-Identifier: MIT

    return itertools.takewhile(
        lambda t: t, map(lambda chunk: fh.read(size), itertools.count(0))
    )
