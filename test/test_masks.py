import unittest
from lib import masks
from lib.masks import Sample


class Mask1d(unittest.TestCase):
    def test_len(self):
        sent = "1, 21, 35, 4"
        samples = list(masks.mask_1d(sent))
        self.assertEqual(len(samples), 6)

    def test_val(self):
        sent = "21, 3"
        targets = [
            Sample(sent="<extra_id_0>1, 3", label="<extra_id_0> 2 <extra_id_1>"),
            Sample(sent="2<extra_id_0>, 3", label="<extra_id_0> 1 <extra_id_1>"),
            Sample(sent="21, <extra_id_0>", label="<extra_id_0> 3 <extra_id_1>"),
        ]
        samples = list(masks.mask_1d(sent))

        is_in = True
        for target in targets:
            if target not in samples:
                is_in = False

        self.assertTrue(is_in, "should generate the correct samples.")
