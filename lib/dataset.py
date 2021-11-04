import tables
from itertools import product
import os.path
from lib import config
from typing import List


def _combine_iter(combinations: List[List[int]], data: List[int]):
    """Returns a cartesian product of combinations and data."""
    combinations_ = []
    for combination in combinations:
        for x in data:
            combinations_.append(combination.append(x))
    return combinations_


def _generate_sentences(nums: List[int]):
    """Generates all possible sentences.

    These sentences cover all possible tasks and sentence formats.
    """
    # Generate all possible task-format pairs.
    tasks = product(config.TASKS.keys(), config.SENT_FORMATS)

    # Stringify the list.
    nums_str = ", ".join([str(num) for num in nums[:-1]]) + " and " + str(nums[-1])

    # For each task, create a sentence.
    sentences = []
    for task_name, sent_format in tasks:
        # Calculate target variable.
        # NOTE: config.TASKS is a dictionary mapping task names to functions.
        target = str(config.TASKS[task_name](nums))

        # Create and append a sentence.
        sentence = sent_format.format(task=task_name, nums_str=nums_str, target=target)
        sentences.append(sentence)

    return sentences


def generate_dataset_all(rewrite: bool = False):
    """Generates a dataset from all possible combinations."""
    # Check if dataset already exists.
    if os.path.exists(config.DATASET_PATH):
        if rewrite:
            os.remove(config.DATASET_PATH)
        else:
            raise FileExistsError("Dataset already exists. Set rewrite=True or delete existing file.")

    # Create the dataset.


    # Create initial combinations

    # For each iteration
        # Create the next set of combinations

        # Generate all possible sentences

        # Create all masked samples in sentence

        # Write all samples to the dataset
