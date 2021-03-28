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

    # SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
    # SPDX-License-Identifier: MIT

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


if __name__ == "__main__":
    print("# Basic repr formatting")
    print("numfmt(12345)")
    print("  = {}".format(numfmt(12345)))
    print('numfmt(12345, fmt="{num.real:0.09f} {num.prefix}")')
    print("  = {}".format(numfmt(12345, fmt="{num.real:0.09f} {num.prefix}")))
    print()
    print("# Positional or named attributes")
    print('"{0.real:0.03f} {0.prefix}B".format(numfmt(12345))')
    print("  = {0.real:0.03f} {0.prefix}B".format(numfmt(12345)))
    print('"{num.real:0.01f} {num.prefix}B/s".format(num=numfmt(12345))')
    print("  = {num.real:0.01f} {num.prefix}B/s".format(num=numfmt(12345)))
    print()
    print("# F-strings")
    print('num = numfmt(12345); f"{num.real:0.04f} {num.prefix}B"')
    num = numfmt(12345)
    print(f"  = {num.real:0.04f} {num.prefix}B")
    print()
    print("# Named attributes, binary SI prefixes")
    print('"{num.real:0.02f} {num.prefix}B".format(num=numfmt(12345, binary=True))')
    print("  = {num.real:0.02f} {num.prefix}B".format(num=numfmt(12345, binary=True)))
    print()
    print("# Rollover before 100% of a normal prefix change")
    print('"{num.real:0.02f} {num.prefix}B".format(num=numfmt(897306, rollover=0.9))')
    print("  = {num.real:0.02f} {num.prefix}B".format(num=numfmt(897306, rollover=0.9)))
    print('"{num.real:0.02f} {num.prefix}B".format(num=numfmt(973829, rollover=0.9))')
    print("  = {num.real:0.02f} {num.prefix}B".format(num=numfmt(973829, rollover=0.9)))
    print()
    print("# Rollover after 100% of a normal prefix change")
    print('"{num.real:0.02f} {num.prefix}B".format(num=numfmt(1032456, rollover=1.1))')
    print(
        "  = {num.real:0.02f} {num.prefix}B".format(num=numfmt(1032456, rollover=1.1))
    )
    print('"{num.real:0.02f} {num.prefix}B".format(num=numfmt(1122334, rollover=1.1))')
    print(
        "  = {num.real:0.02f} {num.prefix}B".format(num=numfmt(1122334, rollover=1.1))
    )
    print()
    print("# Limit number of prefix changes")
    print('"{num.real:0.02f} {num.prefix}B".format(num=numfmt(123000000000, limit=2))')
    print(
        "  = {num.real:0.02f} {num.prefix}B".format(num=numfmt(123000000000, limit=2))
    )
