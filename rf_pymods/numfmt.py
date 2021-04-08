# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT


def numfmt(
    num,
    fmt="{num.real:0.02f} {num.prefix}",
    binary=False,
    rollover=1.0,
    limit=0,
    prefixes=None,
):
    """Formats a number with decimal or binary prefixes

    num: Input number
    fmt: Format string of default repr/str output
    binary: If True, use divide by 1024 and use IEC binary prefixes
    rollover: Threshold to roll over to the next prefix
    limit: Stop after a specified number of rollovers
    prefixes: List of (decimal, binary) prefix strings, ascending
    """
    # SPDX-SnippetComment: Originally from https://github.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
    # SPDX-LicenseInfoInSnippet: MIT

    class NumberFormat(float):
        prefix = ""
        fmt = "{num.real:0.02f} {num.prefix}"

        def __str__(self):
            return self.fmt.format(num=self)

        def __repr__(self):
            return str(self)

    if prefixes is None:
        prefixes = [
            ("k", "Ki"),
            ("M", "Mi"),
            ("G", "Gi"),
            ("T", "Ti"),
            ("P", "Pi"),
            ("E", "Ei"),
            ("Z", "Zi"),
            ("Y", "Yi"),
        ]
    divisor = 1024 if binary else 1000
    if limit <= 0 or limit > len(prefixes):
        limit = len(prefixes)

    count = 0
    p = ""
    for prefix in prefixes:
        if num < (divisor * rollover):
            break
        if count >= limit:
            break
        count += 1
        num = num / float(divisor)
        p = prefix[1] if binary else prefix[0]
    ret = NumberFormat(num)
    ret.fmt = fmt
    ret.prefix = p
    return ret
