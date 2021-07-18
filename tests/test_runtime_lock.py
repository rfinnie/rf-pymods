# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

import errno
import importlib
import unittest
import unittest.mock as mock

from . import decorated_mocks
from rf_pymods.runtime_lock import runtime_lock


def ioerror_eacces():
    e = IOError()
    e.errno = errno.EACCES
    return e


@mock.patch("rf_pymods.runtime_lock.open", new_callable=mock.mock_open)
@mock.patch("rf_pymods.runtime_lock.os.unlink")
@unittest.skipUnless(importlib.util.find_spec("fcntl"), "fcntl required")
class Testruntime_lock(unittest.TestCase):
    @mock.patch("rf_pymods.runtime_lock.fcntl.lockf")
    @decorated_mocks
    def test_lock(self, mocks):
        with runtime_lock():
            pass
        mocks["open"].assert_called_once()
        mocks["open"]().write.assert_called_once()

    @mock.patch("rf_pymods.runtime_lock.fcntl.lockf", side_effect=ioerror_eacces())
    @decorated_mocks
    def test_lockf_eacces(self, mocks):
        with self.assertRaises(IOError):
            runtime_lock()

    @mock.patch("rf_pymods.runtime_lock.fcntl.lockf")
    @mock.patch("rf_pymods.runtime_lock.os.path.exists", return_value=False)
    @decorated_mocks
    def test_no_suitable_lock_dir(self, mocks):
        with self.assertRaises(FileNotFoundError):
            runtime_lock()

    @mock.patch("rf_pymods.runtime_lock.fcntl.lockf")
    @mock.patch("rf_pymods.runtime_lock.sys.argv", [""])
    @decorated_mocks
    def test_empty_argv(self, mocks):
        runtime_lock()
