# SPDX-FileCopyrightText: Copyright (C) 2020-2021 Ryan Finnie
# SPDX-License-Identifier: MIT

from datetime import datetime, timedelta
from unittest import TestCase

from rf_pymods.croniter_hash import croniter, croniter_hash


class TestCroniterHash(TestCase):
    epoch = datetime(2020, 1, 1, 0, 0)
    hash_id = "hello"

    def _test_iter(
        self, definition, expectations, delta, epoch=None, hash_id=None, next_type=None
    ):
        if epoch is None:
            epoch = self.epoch
        if hash_id is None:
            hash_id = self.hash_id
        if next_type is None:
            next_type = datetime
        if not isinstance(expectations, (list, tuple)):
            expectations = (expectations,)
        obj = croniter_hash(definition, epoch, hash_id=hash_id)
        testval = obj.get_next(next_type)
        self.assertIn(testval, expectations)
        if delta is not None:
            self.assertEqual(obj.get_next(next_type), testval + delta)

    def test_hash_hourly(self):
        """Test manually-defined hourly"""
        self._test_iter("H * * * *", datetime(2020, 1, 1, 0, 10), timedelta(hours=1))

    def test_hash_daily(self):
        """Test manually-defined daily"""
        self._test_iter("H H * * *", datetime(2020, 1, 1, 11, 10), timedelta(days=1))

    def test_hash_weekly(self):
        """Test manually-defined weekly"""
        # croniter 1.0.5 changes the defined weekly range from (0, 6)
        # to (0, 7), to match cron's behavior that Sunday is 0 or 7.
        # This changes our hash, so test for either.
        self._test_iter(
            "H H * * H",
            (datetime(2020, 1, 3, 11, 10), datetime(2020, 1, 5, 11, 10)),
            timedelta(weeks=1),
        )

    def test_hash_monthly(self):
        """Test manually-defined monthly"""
        self._test_iter("H H H * *", datetime(2020, 1, 1, 11, 10), timedelta(days=31))

    def test_hash_yearly(self):
        """Test manually-defined yearly"""
        self._test_iter("H H H H *", datetime(2020, 9, 1, 11, 10), timedelta(days=365))

    def test_hash_word_midnight(self):
        """Test built-in @midnight

        @midnight is actually up to 3 hours after midnight, not exactly midnight
        """
        self._test_iter("@midnight", datetime(2020, 1, 1, 2, 10, 32), timedelta(days=1))

    def test_hash_word_hourly(self):
        """Test built-in @hourly"""
        self._test_iter("@hourly", datetime(2020, 1, 1, 0, 10, 32), timedelta(hours=1))

    def test_hash_word_daily(self):
        """Test built-in @daily"""
        self._test_iter("@daily", datetime(2020, 1, 1, 11, 10, 32), timedelta(days=1))

    def test_hash_word_weekly(self):
        """Test built-in @weekly"""
        # croniter 1.0.5 changes the defined weekly range from (0, 6)
        # to (0, 7), to match cron's behavior that Sunday is 0 or 7.
        # This changes our hash, so test for either.
        self._test_iter(
            "@weekly",
            (datetime(2020, 1, 3, 11, 10, 32), datetime(2020, 1, 5, 11, 10, 32)),
            timedelta(weeks=1),
        )

    def test_hash_word_monthly(self):
        """Test built-in @monthly"""
        self._test_iter(
            "@monthly", datetime(2020, 1, 1, 11, 10, 32), timedelta(days=31)
        )

    def test_hash_word_yearly(self):
        """Test built-in @yearly"""
        self._test_iter(
            "@yearly", datetime(2020, 9, 1, 11, 10, 32), timedelta(days=365)
        )

    def test_hash_word_annually(self):
        """Test built-in @annually

        @annually is the same as @yearly
        """
        obj_annually = croniter_hash("@annually", self.epoch, hash_id=self.hash_id)
        obj_yearly = croniter_hash("@yearly", self.epoch, hash_id=self.hash_id)
        self.assertEqual(obj_annually.get_next(datetime), obj_yearly.get_next(datetime))
        self.assertEqual(obj_annually.get_next(datetime), obj_yearly.get_next(datetime))

    def test_hash_second(self):
        """Test seconds

        If a sixth field is provided, seconds are included in the datetime()
        """
        self._test_iter(
            "H H * * * H", datetime(2020, 1, 1, 11, 10, 32), timedelta(days=1)
        )

    def test_hash_id_change(self):
        """Test a different hash_id returns different results given same definition and epoch"""
        self._test_iter("H H * * *", datetime(2020, 1, 1, 11, 10), timedelta(days=1))
        self._test_iter(
            "H H * * *",
            datetime(2020, 1, 1, 0, 24),
            timedelta(days=1),
            hash_id="different id",
        )

    def test_hash_epoch_change(self):
        """Test a different epoch returns different results given same definition and hash_id"""
        self._test_iter("H H * * *", datetime(2020, 1, 1, 11, 10), timedelta(days=1))
        self._test_iter(
            "H H * * *",
            datetime(2011, 11, 12, 11, 10),
            timedelta(days=1),
            epoch=datetime(2011, 11, 11, 11, 11),
        )

    def test_hash_range(self):
        """Test a hashed range definition"""
        self._test_iter(
            "H H H(3-5) * *", datetime(2020, 1, 5, 11, 10), timedelta(days=31)
        )

    def test_hash_id_bytes(self):
        """Test hash_id as a bytes object"""
        self._test_iter(
            "H H * * *",
            datetime(2020, 1, 1, 14, 53),
            timedelta(days=1),
            hash_id=b"\x01\x02\x03\x04",
        )

    def test_hash_float(self):
        """Test result as a float object"""
        self._test_iter("H H * * *", 1577877000.0, (60 * 60 * 24), next_type=float)

    def test_random(self):
        """Test random definition"""
        obj = croniter_hash("R R * * *", self.epoch, hash_id=self.hash_id)
        result_1 = obj.get_next(datetime)
        self.assertGreaterEqual(result_1, datetime(2020, 1, 1, 0, 0))
        self.assertLessEqual(result_1, datetime(2020, 1, 1, 0, 0) + timedelta(days=1))
        result_2 = obj.get_next(datetime)
        self.assertGreaterEqual(result_2, datetime(2020, 1, 2, 0, 0))
        self.assertLessEqual(result_2, datetime(2020, 1, 2, 0, 0) + timedelta(days=1))

    def test_random_range(self):
        """Test random definition within a range"""
        obj = croniter_hash("R R R(10-20) * *", self.epoch, hash_id=self.hash_id)
        result_1 = obj.get_next(datetime)
        self.assertGreaterEqual(result_1, datetime(2020, 1, 10, 0, 0))
        self.assertLessEqual(result_1, datetime(2020, 1, 10, 0, 0) + timedelta(days=11))
        result_2 = obj.get_next(datetime)
        self.assertGreaterEqual(result_2, datetime(2020, 2, 10, 0, 0))
        self.assertLessEqual(result_2, datetime(2020, 2, 10, 0, 0) + timedelta(days=11))

    def test_random_float(self):
        """Test random definition, float result"""
        obj = croniter_hash("R R * * *", self.epoch, hash_id=self.hash_id)
        result_1 = obj.get_next(float)
        self.assertGreaterEqual(result_1, 1577836800.0)
        self.assertLessEqual(result_1, 1577836800.0 + (60 * 60 * 24))
        result_2 = obj.get_next(float)
        self.assertGreaterEqual(result_2, 1577923200.0)
        self.assertLessEqual(result_2, 1577923200.0 + (60 * 60 * 24))

    def test_cron(self):
        """Test standard croniter functionality"""
        self._test_iter("35 6 * * *", datetime(2020, 1, 1, 6, 35), timedelta(days=1))

    def test_invalid_definition(self):
        """Test an invalid defition raises CroniterNotAlphaError"""
        with self.assertRaises(croniter.CroniterNotAlphaError):
            croniter_hash("X X * * *", self.epoch, hash_id=self.hash_id)

    def test_invalid_get_next_type(self):
        """Test an invalid get_next type raises TypeError"""
        obj = croniter_hash("H H * * *", self.epoch, hash_id=self.hash_id)
        with self.assertRaises(TypeError):
            obj.get_next(str)

    def test_invalid_hash_id_type(self):
        """Test an invalid hash_id type raises TypeError"""
        with self.assertRaises(TypeError):
            croniter_hash("H H * * *", self.epoch, hash_id={1: 2})
