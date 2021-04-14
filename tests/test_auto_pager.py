# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import unittest
import unittest.mock as mock

from rf_pymods.auto_pager import AutoPager


class TestAutoPager(unittest.TestCase):
    @mock.patch("rf_pymods.auto_pager.subprocess.Popen")
    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=True)
    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "", "LESS": ""})
    def test_pager(self, m_isatty, m_popen):
        """Test TTY, default pager"""
        with AutoPager() as pager:
            for i in range(1000):
                print(i, file=pager)
        m_popen.assert_called_once()
        self.assertEqual(m_popen.call_args[0], (["pager"],))
        self.assertEqual(pager.pager, m_popen())
        # print() gives the \n to write() separately, so 2x number
        # of print()s
        self.assertEqual(pager.pager.stdin.write.call_count, 2000)

    @mock.patch("rf_pymods.auto_pager.subprocess.Popen")
    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=True)
    @mock.patch.dict(
        "rf_pymods.auto_pager.os.environ", {"PAGER": "altpager", "LESS": ""}
    )
    def test_pager_cmd_env(self, m_isatty, m_popen):
        """Test TTY, PAGER=altpager"""
        with AutoPager() as pager:
            print("foo", file=pager)
        m_popen.assert_called_once()
        self.assertEqual(m_popen.call_args[0], (["altpager"],))

    @mock.patch("rf_pymods.auto_pager.subprocess.Popen")
    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=False)
    @mock.patch("rf_pymods.auto_pager.sys.stdout")
    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "", "LESS": ""})
    def test_pager_notty(self, m_stdout, m_isatty, m_popen):
        """Test no TTY (stdout)"""
        with AutoPager() as pager:
            print("foo", file=pager)
        m_popen.assert_not_called()
        self.assertEqual(pager.pager, None)
        # print() gives the \n to write() separately, so 2x number
        # of print()s
        self.assertEqual(m_stdout.write.call_count, 2)

    @mock.patch("rf_pymods.auto_pager.subprocess.Popen", side_effect=FileNotFoundError)
    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=True)
    @mock.patch.dict(
        "rf_pymods.auto_pager.os.environ", {"PAGER": "notfound", "LESS": ""}
    )
    def test_pager_notfound(self, m_isatty, m_popen):
        """Test Popen() returning FileNotFoundError (fallback to stdout)"""
        with AutoPager() as pager:
            print("foo", file=pager)
        m_popen.assert_called_once()
        self.assertEqual(pager.pager, None)

    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=False)
    @mock.patch("rf_pymods.auto_pager.sys.stdout")
    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "", "LESS": ""})
    def test_write(self, m_stdout, m_isatty):
        """Test direct write()"""
        with AutoPager() as pager:
            pager.write("foo")
        self.assertEqual(m_stdout.write.call_count, 1)

    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=False)
    @mock.patch("rf_pymods.auto_pager.sys.stdout")
    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "", "LESS": ""})
    def test_write_closed(self, m_stdout, m_isatty):
        """Test writing to a closed handle doesn't attempt an underlying write"""
        with AutoPager() as pager:
            pager.close()
            print("foo", file=pager)
        m_stdout().write.assert_not_called()

    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=False)
    @mock.patch("rf_pymods.auto_pager.sys.stdout.write", side_effect=KeyboardInterrupt)
    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "", "LESS": ""})
    def test_write_keyboardinterrupt(self, m_write, m_isatty):
        """Test KeyboardInterrupt during write() closes pager"""
        with AutoPager() as pager:
            print("foo", file=pager)
            self.assertEqual(pager.closed, True)
            m_write.assert_called_once()

    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=False)
    @mock.patch("rf_pymods.auto_pager.sys.stdout.write", side_effect=BrokenPipeError)
    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "", "LESS": ""})
    def test_write_brokenpipeerror(self, m_write, m_isatty):
        """Test BrokenPipeError during write() closes pager"""
        with AutoPager() as pager:
            print("foo", file=pager)
            self.assertEqual(pager.closed, True)
            m_write.assert_called_once()

    @mock.patch("rf_pymods.auto_pager.subprocess.Popen")
    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=True)
    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "", "LESS": ""})
    def test_close_keyboardinterrupt(self, m_isatty, m_popen):
        """Test KeyboardInterrupt during close() is ignored"""
        with AutoPager() as pager:
            pager.pager.wait = mock.MagicMock(
                side_effect=[None, KeyboardInterrupt, None, 127]
            )
            print("foo", file=pager)
        self.assertEqual(pager.closed, True)
        self.assertEqual(pager.pager.wait.call_count, 4)

    @mock.patch("rf_pymods.auto_pager.subprocess.Popen")
    @mock.patch("rf_pymods.auto_pager.sys.stdout.isatty", return_value=True)
    @mock.patch.dict("rf_pymods.auto_pager.os.environ", {"PAGER": "", "LESS": ""})
    def test_close_brokenpipeerror(self, m_isatty, m_popen):
        """Test BrokenPipeError during close() is ignored"""
        with AutoPager() as pager:
            pager.pager.stdin.close = mock.MagicMock(side_effect=BrokenPipeError)
            print("foo", file=pager)
        self.assertEqual(pager.closed, True)
        pager.pager.stdin.close.assert_called_once()
