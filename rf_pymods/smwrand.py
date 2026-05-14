# SPDX-PackageName: rf-pymods
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://forge.colobox.com/rfinnie/rf-pymods
# SPDX-FileCopyrightText: © 2019 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT


class SMWRand:
    """Super Mario World random number generator

    Based on deconstruction by Retro Game Mechanics Explained
    https://www.youtube.com/watch?v=q15yNrJHOak
    """

    # SPDX-SnippetComment: Originally from https://forge.colobox.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: © 2019 Ryan Finnie <ryan@finnie.org>
    # SPDX-LicenseInfoInSnippet: MIT

    seed_1 = 0
    seed_2 = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _rand(self):
        self.seed_1 = (self.seed_1 + (self.seed_1 << 2) + 1) & 0xFF
        self.seed_2 = ((self.seed_2 << 1) + int((self.seed_2 & 0x90) in (0x90, 0))) & 0xFF
        return self.seed_1 ^ self.seed_2

    def rand(self):
        output_2 = self._rand()
        output_1 = self._rand()
        return (output_1, output_2)
