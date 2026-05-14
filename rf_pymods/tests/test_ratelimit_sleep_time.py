# SPDX-PackageName: rf-pymods
# SPDX-PackageSupplier: Ryan Finnie <ryan@finnie.org>
# SPDX-PackageDownloadLocation: https://forge.colobox.com/rfinnie/rf-pymods
# SPDX-FileCopyrightText: © 2026 Ryan Finnie <ryan@finnie.org>
# SPDX-License-Identifier: MIT

import datetime
import types
from unittest import TestCase

from rf_pymods.ratelimit_sleep_time import ratelimit_sleep_time


class TestRatelimitSleepTime(TestCase):
    def test_no_ratelimit(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response), datetime.timedelta(seconds=0))

    def test_invalid_response(self):
        response = {}
        with self.assertRaises(AttributeError):
            ratelimit_sleep_time(response)

    def test_iso8601_reset(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "1980",
                "x-ratelimit-reset": "2026-05-14T19:42:06Z",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response), datetime.timedelta(microseconds=595))

    def test_epoch_seconds_reset(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "1980",
                "x-ratelimit-reset": "1778787726",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response), datetime.timedelta(microseconds=595))

    def test_epoch_milliseconds_reset(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "1980",
                "x-ratelimit-reset": "1778787726000",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response), datetime.timedelta(microseconds=595))

    def test_delta_reset(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "1980",
                "x-ratelimit-reset": "270",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response), datetime.timedelta(microseconds=595))

    def test_negative_reset(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "1980",
                "x-ratelimit-reset": "2026-05-14T19:37:30Z",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response), datetime.timedelta(seconds=1))

    def test_no_accel(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "1980",
                "x-ratelimit-reset": "2026-05-14T19:42:06Z",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response, accel=1), datetime.timedelta(microseconds=136295))

    def test_spillover(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "1",
                "x-ratelimit-reset": "2026-05-14T19:37:37Z",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response), datetime.timedelta(seconds=2))

    def test_zero_remaining(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "0",
                "x-ratelimit-reset": "2026-05-14T19:42:06Z",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response), datetime.timedelta(seconds=271))

    def test_negative_remaining(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "-10",
                "x-ratelimit-reset": "2026-05-14T19:42:06Z",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response), datetime.timedelta(seconds=271))

    def test_leniency(self):
        response = types.SimpleNamespace(
            headers={
                "date": "Thu, 14 May 2026 19:37:36 GMT",
                "x-ratelimit-limit": "2000",
                "x-ratelimit-remaining": "0",
                "x-ratelimit-reset": "2026-05-14T19:42:06Z",
            }
        )
        self.assertEqual(ratelimit_sleep_time(response, leniency=0), datetime.timedelta(seconds=270))
