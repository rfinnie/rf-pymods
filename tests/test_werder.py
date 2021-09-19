# SPDX-FileCopyrightText: Copyright (C) 2021 Ryan Finnie
# SPDX-License-Identifier: MIT

from unittest import TestCase
from unittest.mock import patch

from rf_pymods import werder


class TestWerder(TestCase):
    def test_werd(self):
        """Test werd() produces a correct-looking werd"""
        w = werder.Werder()
        self.assertGreaterEqual(len(w.werd()), w.syllables_min)

    def test_werd_coverage(self):
        """Get complete werd() coverage"""
        w = werder.Werder()
        for intval in range(3):
            with patch.object(werder.random, "randint", return_value=intval):
                w.werd()

    def test_sentence(self):
        """Test sentence() produces a correctl-looking sentence"""
        w = werder.Werder()
        sentence_parts = w.sentence().split(" ")
        self.assertGreaterEqual(len(sentence_parts), w.werds_min)
        self.assertLessEqual(len(sentence_parts), w.werds_max)

    def test_main(self):
        """Test main entry point"""
        with patch.object(werder, "print") as mock_print:
            werder.main()
        mock_print.assert_called_once()

    def test__init(self):
        """Testable __main__"""
        with patch.object(werder, "main", return_value=0), patch.object(
            werder, "__name__", "__main__"
        ), patch.object(werder.sys, "exit") as mock_exit:
            werder._init()
        self.assertEqual(mock_exit.call_args[0][0], 0)
