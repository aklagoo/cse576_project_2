import unittest
from lib import masks


class Mask1d(unittest.TestCase):
    def test_len(self):
        sent = "1, 21, 35, 4"
        samples = list(masks.mask_1d(sent))
        self.assertEqual(len(samples), 6)
