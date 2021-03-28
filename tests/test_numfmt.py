from unittest import TestCase

from rf_pymods.numfmt import numfmt


class TestNumfmt(TestCase):
    def test_format(self):
        self.assertEqual("{}".format(numfmt(12345)), "12.35 k")

    def test_numfmt_fmt(self):
        self.assertEqual(
            "{}".format(numfmt(12345, fmt="{num.real:0.09f} {num.prefix}")),
            "12.345000000 k",
        )

    def test_positional_num(self):
        self.assertEqual(
            "{0.real:0.03f} {0.prefix}B".format(numfmt(12345)), "12.345 kB"
        )

    def test_positional_named(self):
        self.assertEqual(
            "{num.real:0.01f} {num.prefix}B/s".format(num=numfmt(12345)), "12.3 kB/s"
        )

    def test_fstring(self):
        num = numfmt(12345)
        self.assertEqual(f"{num.real:0.04f} {num.prefix}B", "12.3450 kB")

    def test_binary_si_prefix(self):
        self.assertEqual(
            "{num.real:0.02f} {num.prefix}B".format(num=numfmt(12345, binary=True)),
            "12.06 KiB",
        )

    def test_rollover_before_prefix_change(self):
        self.assertEqual(
            "{num.real:0.02f} {num.prefix}B".format(num=numfmt(897306, rollover=0.9)),
            "897.31 kB",
        )
        self.assertEqual(
            "{num.real:0.02f} {num.prefix}B".format(num=numfmt(973829, rollover=0.9)),
            "0.97 MB",
        )

    def test_rollover_after_prefix_change(self):
        self.assertEqual(
            "{num.real:0.02f} {num.prefix}B".format(num=numfmt(1032456, rollover=1.1)),
            "1032.46 kB",
        )
        self.assertEqual(
            "{num.real:0.02f} {num.prefix}B".format(num=numfmt(1122334, rollover=1.1)),
            "1.12 MB",
        )

    def test_limit_prefix_changes(self):
        self.assertEqual(
            "{num.real:0.02f} {num.prefix}B".format(num=numfmt(123000000000, limit=2)),
            "123000.00 MB",
        )
