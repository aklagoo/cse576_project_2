"""This module contains functions for formatting data.

A formatting function generates a single sentence for the passed task, numbers,
and target. Each function accepts three arguments: the task (task_name) as
defined in config.TASKS, a list of input numbers, and the target value. The
function returns a single sentence as a formatted string. A sample definition
is as follows:

def format_N(task_name: str, nums: List[int], target: int) -> str:
    ...
"""
from typing import List


def format_1(task_name: str, nums: List[int], target: int) -> str:
    """Returns a sentence with format 1.

    Example:
        The maximum value among 1, 2, 3, 4, and 5 is 5.
    """
    # Stringify the list.
    nums_str = ", ".join([str(num) for num in nums[:-1]]) + ", and " + str(nums[-1])

    # Generate the sentence
    sentence = "The {task} value among {nums_str} is {target}.".format(
        task=task_name, nums_str=nums_str, target=target
    )
    return sentence


# List of all formats
formats = {
    'format_1': format_1,
}
