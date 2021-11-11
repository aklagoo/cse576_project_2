import unittest
from src import formats


class Format1(unittest.TestCase):
    def test_formatting(self):
        sent = formats.format_1('maximum', [1, 2, 3], 3)
        self.assertEqual("The maximum value among 1, 2, and 3 is 3.", sent, "should create the correct sentence.")
