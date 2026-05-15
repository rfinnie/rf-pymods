# SPDX-PackageName: rf-pymods
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://forge.colobox.com/rfinnie/rf-pymods
# SPDX-FileCopyrightText: © 2021 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT


# SPDX-SnippetBegin
# SPDX-SnippetName: ewma from rf-pymods
# SPDX-SnippetComment: Originally from https://forge.colobox.com/rfinnie/rf-pymods
# SPDX-SnippetCopyrightText: © 2021 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT
class EWMA:
    """Exponentially-weighted moving average

    vals: Number, or list of numbers to add
    weight: Moving average weight, default 8.0
    """

    average = 1.0
    weight = 8.0
    items = 0
    sum = 0

    def __init__(self, vals=None, weight=8.0):
        self.weight = weight
        if vals is not None:
            self.add(vals)

    def __len__(self):
        return self.items

    def __float__(self):
        return self.average

    def __int__(self):
        return int(self.average)

    def add(self, vals):
        """Add one or more numbers to the weighted average, in place

        vals: Number, or list of numbers
        """
        if isinstance(vals, (int, float, complex)):
            vals = [vals]
        for number in vals:
            self.average = (1 / self.weight) * number + (1 - (1 / self.weight)) * self.average
            self.items += 1
            self.sum += number

    def append(self, vals):
        self.add(vals)

    def extend(self, vals):
        self.add(vals)


# SPDX-SnippetEnd
