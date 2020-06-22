import io
import unittest

from rf_pymods.readiter import readiter


class TestReaditer(unittest.TestCase):
    def test_short(self):
        fh = io.StringIO("?" * 10)
        self.assertEqual([x for x in readiter(fh)], ["?" * 10])

    def test_one(self):
        fh = io.StringIO("?" * 1024)
        self.assertEqual([x for x in readiter(fh)], ["?" * 1024])

    def test_one_plus_partial(self):
        fh = io.StringIO(("?" * 1024) + ("!" * 15))
        self.assertEqual([x for x in readiter(fh)], ["?" * 1024, "!" * 15])

    def test_two(self):
        fh = io.StringIO(("?" * 1024) + ("!" * 1024))
        self.assertEqual([x for x in readiter(fh)], ["?" * 1024, "!" * 1024])

    def test_size(self):
        fh = io.StringIO(("?" * 10) + ("!" * 15))
        self.assertEqual(
            [x for x in readiter(fh, size=10)], ["?" * 10, "!" * 10, "!" * 5]
        )

    def test_bytes(self):
        fh = io.BytesIO(bytes(1024))
        self.assertEqual([x for x in readiter(fh)], [bytes(1024)])
