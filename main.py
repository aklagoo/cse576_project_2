"""This module is a command-line script for all functions."""
import random
import csv
from lib import config


def combine_iter(combinations, data):
    combinations_ = []
    for combination in combinations:
        for x in data:
            combinations_.append(combination.append(x))
    return combinations_


def generate_all_samples():
    """Generate samples and write to a file."""
    with open(config.DATASET_PATH, mode='w') as file:
        # Create writer
        writer = csv.DictWriter(file, fieldnames=config.DATASET_COLS)
        writer.writeheader()

        # Initialize data
        data = list(range(*config.NUMS_VAL_RANGE))
        idx_start, idx_end = config.NUMS_LEN_RANGE[0], config.NUMS_LEN_RANGE[1]
        combinations = [[x] for x in data]
        for _ in range(2, idx_start - 1):
            combinations = combine_iter(combinations, data)

        # Create and write samples
        for _ in range(idx_end - idx_start + 1):
            combinations_ = combinations.copy()
            


def generate_sample():
    """Randomly generates a sample."""
    # Generate task randomly
    nums_len = random.randint(*config.NUMS_LEN_RANGE)
    nums = [random.randrange(*config.NUMS_VAL_RANGE) for _ in range(nums_len)]
    task = random.choice(config.TASKS)
    sent_format = random.choice(config.SENT_FORMATS)

    # Stringify list and identify target number
    nums_str = ", ".join([str(num) for num in nums[:-1]])
    nums_str = nums_str + " and " + str(nums[-1])
    if task == "minimum":
        nums_target = str(min(nums))
    elif task == "maximum":
        nums_target = str(max(nums))
    else:
        raise KeyError("Invalid type of task. Valid options are: \"minimum\" and \"maximum\".")

    return sent_format.format(task=task, nums_str=nums_str, nums_target=nums_target)


if __name__ == '__main__':
    print(generate_sample())
