import unittest
from lib import dataset


class DatasetCombineIter(unittest.TestCase):
    COMBINATIONS = [[1], [2]]
    DATA = [1, 2]

    def test_len(self):
        combinations = dataset._combine_iter(self.COMBINATIONS, self.DATA)
        self.assertEqual(len(combinations), 4, "should generate the correct number of combinations")

    def test_val(self):
        combinations = dataset._combine_iter(self.COMBINATIONS, self.DATA)
        targets = [
            [1, 1],
            [1, 2],
            [2, 1],
            [2, 2],
        ]
        is_in = True
        for target in targets:
            if target not in combinations:
                is_in = False
                break

        self.assertTrue(is_in, "should generate all possible combinations.")


class DatasetGenerateRandom(unittest.TestCase):
    pass
