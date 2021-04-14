# SPDX-FileCopyrightText: Copyright (C) 2021 Ryan Finnie
# SPDX-License-Identifier: MIT

from unittest import TestCase

from rf_pymods.ewma import EWMA


class TestEWMA(TestCase):
    def test_average(self):
        self.assertEqual(EWMA([1, 2, 3]).average, 1.359375)

    def test_weight(self):
        self.assertEqual(EWMA([1, 2, 3], weight=20.0).average, 1.1475)

    def test_add_one(self):
        a = EWMA([1, 2])
        a.add(3)
        self.assertEqual(a.average, 1.359375)

    def test_add_list(self):
        a = EWMA([1])
        a.add([2, 3])
        self.assertEqual(a.average, 1.359375)

    def test_len(self):
        self.assertEqual(len(EWMA([1, 2, 3])), 3)

    def test_float(self):
        self.assertEqual(float(EWMA([1, 2, 3])), 1.359375)

    def test_int(self):
        self.assertEqual(int(EWMA([1, 2, 3])), 1)

    def test_append(self):
        a = EWMA([1])
        a.append([2, 3])
        self.assertEqual(a.average, 1.359375)

    def test_extend(self):
        a = EWMA([1])
        a.extend([2, 3])
        self.assertEqual(a.average, 1.359375)

    def test_sum(self):
        self.assertEqual(EWMA([1, 2, 3]).sum, 6)
