# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import unittest
import unittest.mock as mock

from . import decorated_mocks
from rf_pymods.safe_write import safe_write


@mock.patch("rf_pymods.safe_write.open", new_callable=mock.mock_open)
@mock.patch("rf_pymods.safe_write.os.rename")
@mock.patch("rf_pymods.safe_write.os.path.exists", return_value=False)
@mock.patch("rf_pymods.safe_write.shutil.copystat")
class TestSafeWrite(unittest.TestCase):
    @decorated_mocks
    def test_write(self, mocks):
        with safe_write("testfile") as f:
            f.write("testdata")
        f.closed = False
        f.close()
        mocks["open"].assert_called_once()
        mocks["open"]().write.assert_called_once_with("testdata")
        self.assertEqual(f.original_name, "testfile")

    @decorated_mocks
    def test_close(self, mocks):
        f = safe_write("foo")
        f.closed = False
        f.close()
        mocks["rename"].assert_called_once()

    @decorated_mocks
    def test_already_closed(self, mocks):
        f = safe_write("foo")
        f.closed = True
        f.close()
        mocks["rename"].assert_not_called()

    @decorated_mocks
    def test_preserve_stats(self, mocks):
        mocks["exists"].return_value = True
        with safe_write("foo", preserve_stats=True):
            pass
        mocks["copystat"].assert_called_once()

    @decorated_mocks
    def test_no_preserve_stats(self, mocks):
        mocks["exists"].return_value = True
        with safe_write("foo", preserve_stats=False):
            pass
        mocks["copystat"].assert_not_called()
