# SPDX-FileCopyrightText: Copyright (C) 2018-2021 Ryan Finnie
# SPDX-License-Identifier: MIT
#
# A 2021 rewrite of a 2018 Python port of a 2008 PHP port of a 1998 C
# program. (Sorry, I didn't have the patience to wait until 2028 to
# continue the pattern.)
#
# Original C header:
#
#     Snoof Generator v1.1
#
#     Dave Olszewski  4/25/1997
#     updated         8/12/1998
#
#     A relatively inefficient way
#      to make snoof
#
# The original code did not include any copyright notice, and the
# original author has not responded to a request for clarification.
# However, this port has been effectively 100% rewritten from the
# original C code that it can be considered completely separate
# software, and so is explicitly licensed MIT.

import random
import sys


class Werder:
    """Generate random (but pronounceable) werds"""

    # SPDX-SnippetComment: Originally from https://github.com/rfinnie/rf-pymods
    # SPDX-SnippetCopyrightText: Copyright (C) 2018-2021 Ryan Finnie
    # SPDX-LicenseInfoInSnippet: MIT

    parts_vowel = "a a ai e e ea ee i i ie io o o oa oi oo ou u u".split(" ")
    parts_begin = "b bl cl cr dr fl fr gr k l m pl qu sl sn spl squ tr wr".split(" ")
    parts_end = (
        "ch ck d ff gh ght ll ls ly m mn nct nd ng nt ny rd rt sk st t w zz".split(" ")
    )
    parts_rest = (
        "b c cr ct d f g h k l m n nk p ph r s sh sn sp st str t th v w x z".split(" ")
    )
    werds_min = 5
    werds_max = 9
    syllables_min = 3
    syllables_max = 7

    def werd(self, syllables=-1):
        """Return a werd
        If syllables is -1 (default) a random number of syllables are
        selected.
        """

        werd = ""
        if syllables == -1:
            syllables = random.randint(self.syllables_min, self.syllables_max)

        # Start with a consonant 2/3 of the time
        flip = random.randint(0, 2)

        for syllable in range(syllables):
            # Flip between consonants and vowels
            if (flip + syllable) % 2:
                werd += random.choice(self.parts_vowel)
            elif syllable == 0:
                werd += random.choice(self.parts_begin)
            elif syllable == syllables - 1:
                werd += random.choice(self.parts_end)
            else:
                werd += random.choice(self.parts_rest)

        return werd

    def sentence(self, werds=-1):
        """Return a werder sentence
        If werds is -1 (default) a random number of werds are selected.
        """

        if werds == -1:
            werds = random.randint(self.werds_min, self.werds_max)

        return " ".join(
            [self.werd() for _ in range(werds)]
        ).capitalize() + random.choice(["!", ".", "?"])


def main():
    """Primary interactive entry"""
    print(Werder().sentence())


def _init():
    """Testable __main__ entry function"""
    if __name__ == "__main__":
        sys.exit(main())


_init()
