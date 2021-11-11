import unittest
from src.data import dataset, masks


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


class DatasetGenerate(unittest.TestCase):
    def test_all(self):
        # Generate target samples
        target_sents = [
            "The maximum value among 1, and 1 is 1.",
            "The maximum value among 1, and 2 is 2.",
            "The maximum value among 2, and 1 is 2.",
            "The maximum value among 2, and 2 is 2.",
        ]
        target_samples = []
        for target_sent in target_sents:
            target_samples.extend(masks.mask_1d(target_sent))
        samples = list(dataset._generate_samples_all('format_1', 'mask_1d', 'maximum', (1, 3), (2, 3)))
        is_in = True
        for target in target_samples:
            if target not in samples:
                is_in = False
                break

        self.assertTrue(is_in, "should generate all possible samples.")

    def test_random_len(self):
        samples = samples = list(dataset._generate_samples_random(10, 'format_1', 'mask_1d', 'maximum', (1, 3), (2, 3)))
        self.assertEqual(10, len(samples), "should generate the correct number of samples.")

    def test_random_val(self):
        # Generate target samples
        target_sents = [
            "The maximum value among 1, and 1 is 1.",
            "The maximum value among 1, and 2 is 2.",
            "The maximum value among 2, and 1 is 2.",
            "The maximum value among 2, and 2 is 2.",
        ]
        target_samples = []
        for target_sent in target_sents:
            target_samples.extend(masks.mask_1d(target_sent))
        samples = list(dataset._generate_samples_random(10, 'format_1', 'mask_1d', 'maximum', (1, 3), (2, 3)))

        # Check if samples are a subset of the target samples
        is_subset = set(samples).issubset(set(target_samples))
        print(samples)
        self.assertTrue(is_subset, "should generate some correct values.")

