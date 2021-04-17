# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import unittest
import unittest.mock as mock

from . import decorated_mocks
from rf_pymods.auto_pager import AutoPager


@mock.patch("rf_pymods.auto_pager.subprocess.Popen")
@mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=False)
@mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "", "LESS": ""})
@mock.patch("rf_pymods.auto_pager.sys.stdout")
class TestAutoPager(unittest.TestCase):
    @decorated_mocks
    def test_pager(self, mocks):
        """Test TTY, default pager"""
        mocks["isatty"].return_value = True
        with AutoPager() as pager:
            for i in range(1000):
                print(i, file=pager)
        mocks["Popen"].assert_called_once()
        self.assertEqual(mocks["Popen"].call_args[0], (["pager"],))
        self.assertEqual(pager.pager, mocks["Popen"]())
        # print() gives the \n to write() separately, so 2x number
        # of print()s
        self.assertEqual(pager.pager.stdin.write.call_count, 2000)

    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "altpager"})
    @decorated_mocks
    def test_pager_cmd_env(self, mocks):
        """Test TTY, PAGER=altpager"""
        mocks["isatty"].return_value = True
        with AutoPager() as pager:
            print("foo", file=pager)
        mocks["Popen"].assert_called_once()
        self.assertEqual(mocks["Popen"].call_args[0], (["altpager"],))

    @decorated_mocks
    def test_pager_notty(self, mocks):
        """Test no TTY (stdout)"""
        with AutoPager() as pager:
            print("foo", file=pager)
        mocks["Popen"].assert_not_called()
        self.assertEqual(pager.pager, None)
        # print() gives the \n to write() separately, so 2x number
        # of print()s
        self.assertEqual(mocks["stdout"].write.call_count, 2)

    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "notfound"})
    @decorated_mocks
    def test_pager_notfound(self, mocks):
        """Test Popen() returning FileNotFoundError (fallback to stdout)"""
        mocks["isatty"].return_value = True
        mocks["Popen"].side_effect = FileNotFoundError
        with AutoPager() as pager:
            print("foo", file=pager)
        mocks["Popen"].assert_called_once()
        self.assertEqual(pager.pager, None)

    @decorated_mocks
    def test_write(self, mocks):
        """Test direct write()"""
        with AutoPager() as pager:
            pager.write("foo")
        self.assertEqual(mocks["stdout"].write.call_count, 1)

    @decorated_mocks
    def test_write_closed(self, mocks):
        """Test writing to a closed handle doesn't attempt an underlying write"""
        with AutoPager() as pager:
            pager.close()
            print("foo", file=pager)
        mocks["stdout"]().write.assert_not_called()

    @decorated_mocks
    def test_write_keyboardinterrupt(self, mocks):
        """Test KeyboardInterrupt during write() closes pager"""
        mocks["stdout"].write.side_effect = KeyboardInterrupt
        with AutoPager() as pager:
            print("foo", file=pager)
            self.assertEqual(pager.closed, True)
            mocks["stdout"].write.assert_called_once()

    @decorated_mocks
    def test_write_brokenpipeerror(self, mocks):
        """Test BrokenPipeError during write() closes pager"""
        mocks["stdout"].write.side_effect = BrokenPipeError
        with AutoPager() as pager:
            print("foo", file=pager)
            self.assertEqual(pager.closed, True)
            mocks["stdout"].write.assert_called_once()

    @decorated_mocks
    def test_close_keyboardinterrupt(self, mocks):
        """Test KeyboardInterrupt during close() is ignored"""
        mocks["isatty"].return_value = True
        with AutoPager() as pager:
            pager.pager.wait = mock.MagicMock(
                side_effect=[None, KeyboardInterrupt, None, 127]
            )
            print("foo", file=pager)
        self.assertEqual(pager.closed, True)
        self.assertEqual(pager.pager.wait.call_count, 4)

    @decorated_mocks
    def test_close_brokenpipeerror(self, mocks):
        """Test BrokenPipeError during close() is ignored"""
        mocks["isatty"].return_value = True
        with AutoPager() as pager:
            pager.pager.stdin.close = mock.MagicMock(side_effect=BrokenPipeError)
            print("foo", file=pager)
        self.assertEqual(pager.closed, True)
        pager.pager.stdin.close.assert_called_once()
