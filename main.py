"""This module is a command-line script for all functions."""
import csv
import itertools

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
            combinations = combine_iter(combinations, data)

            # For each combination, generate all possible samples
            for combination in combinations:
                pass


def generate_samples(nums):
    """Generate all possible options"""
    # Generate all possible tasks
    tasks = itertools.product(config.TASKS.keys(), config.SENT_FORMATS)

    # Stringify array
    nums_str = ", ".join([str(num) for num in nums[:-1]])
    nums_str = nums_str + " and " + str(nums[-1])

    # For each task, create a sample
    samples = []
    for task_name, sent_format in tasks:
        target = str(config.TASKS[task_name](nums))
        text = sent_format.format(task=task_name, nums_str=nums_str, target=target)

    return samples


if __name__ == '__main__':
    pass
