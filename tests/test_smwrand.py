# SPDX-FileCopyrightText: Copyright (C) 2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import hashlib
from unittest import TestCase

from rf_pymods.smwrand import SMWRand


class TestSMWRand(TestCase):
    def test_first_run(self):
        """Check first result"""
        with SMWRand() as smwrand:
            self.assertEqual(smwrand.rand(), (5, 0))
            self.assertEqual(smwrand.seed_1, 6)
            self.assertEqual(smwrand.seed_2, 3)

    def test_loop(self):
        """Check known loop

        SMWRand results loop after 27776 runs, so verify #27777 is the
        same as #1.
        """
        smwrand = SMWRand()
        rand_run1 = smwrand.rand()
        seed_1_run1 = smwrand.seed_1
        seed_2_run1 = smwrand.seed_2
        for i in range(27775):
            smwrand.rand()
        self.assertEqual(smwrand.rand(), rand_run1)
        self.assertEqual(smwrand.seed_1, seed_1_run1)
        self.assertEqual(smwrand.seed_2, seed_2_run1)

    def test_all(self):
        """Check all results

        SMWRand results loop after 27776 runs, so we can hash the entire
        output against a known good checksum.
        """
        smwrand = SMWRand()
        a = bytearray()
        for i in range(27776):
            a.extend(smwrand.rand())
        self.assertEqual(
            hashlib.sha256(a).digest(),
            b"\x16+\x05\xb3\xb5f!\xa5\xd5k\xe9Xy\x03\x8d\xffy\xf7l"
            b"\xc6\xef\xc6\x1f\x1e\x85\xd7\xfe\xd7\xbe?\xf3\x0e",
        )
