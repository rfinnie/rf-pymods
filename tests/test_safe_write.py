# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import unittest
import unittest.mock as mock

from rf_pymods.safe_write import safe_write


class TestSafeWrite(unittest.TestCase):
    def test_write(self):
        with mock.patch("rf_pymods.safe_write.open", mock.mock_open()) as m, mock.patch(
            "rf_pymods.safe_write.os.rename"
        ):
            with safe_write("testfile") as f:
                f.write("testdata")
            f.closed = False
            f.close()
        m.assert_called_once()
        m().write.assert_called_once_with("testdata")
        self.assertEqual(f.original_name, "testfile")

    def test_close(self):
        with mock.patch("rf_pymods.safe_write.open", mock.mock_open()), mock.patch(
            "rf_pymods.safe_write.os.rename"
        ) as m_r:
            f = safe_write("foo")
            f.closed = False
            f.close()
        m_r.assert_called()

    def test_already_closed(self):
        with mock.patch("rf_pymods.safe_write.open", mock.mock_open()), mock.patch(
            "rf_pymods.safe_write.os.rename"
        ) as m_r:
            f = safe_write("foo")
            f.closed = True
            f.close()
        m_r.assert_not_called()

    @mock.patch("rf_pymods.safe_write.os.rename")
    @mock.patch("rf_pymods.safe_write.os.path.exists", return_value=True)
    @mock.patch("rf_pymods.safe_write.shutil.copystat")
    def test_preserve_stats(self, m_copystat, m_exists, m_rename):
        with mock.patch("rf_pymods.safe_write.open", mock.mock_open()):
            with safe_write("foo", preserve_stats=True):
                pass
        m_copystat.assert_called_once()

    @mock.patch("rf_pymods.safe_write.os.rename")
    @mock.patch("rf_pymods.safe_write.os.path.exists", return_value=True)
    @mock.patch("rf_pymods.safe_write.shutil.copystat")
    def test_no_preserve_stats(self, m_copystat, m_exists, m_rename):
        with mock.patch("rf_pymods.safe_write.open", mock.mock_open()):
            with safe_write("foo", preserve_stats=False):
                pass
        m_copystat.assert_not_called()
