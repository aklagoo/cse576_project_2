"""This module contains functions for sentence masking.

A masking function masks parts of an input sentence as defined in
"""
import re
from src import config
from typing import Generator, NamedTuple


class Sample(NamedTuple):
    sent: str
    label: str


def mask_one_digit(sentence: str) -> Generator[Sample, None, None]:
    """Masks a single digit.

    Example:
        Original: The maximum of 1, 2, 35, 7, 8 is 35.
        Masked: The maximum of 1, 2, <extra_id_0>5, 7, 8 is 35.

    Args:
        sentence: A sentence to be masked.
    Returns:
        List of samples, such that each sample contains
            sent: A masked sentence.
            targets: The masked part(s) of the input.
    """
    samples = []

    # Find all matches using Regex
    pattern = re.compile(r"\d")
    for match in pattern.finditer(sentence):
        # Extract match
        start, end = match.span()
        text = match.group()

        # Replace match with mask token
        masked = sentence[:start] + config.MASK_TOKEN.format(0) + sentence[end:]
        label = config.MASK_TOKEN.format(0) + " " + text + " " + config.MASK_TOKEN.format(1)

        # Append sample
        yield Sample(sent=masked, label=label)

def mask_one_number(sentence: str) -> Generator[Sample, None, None]:
    """Masks the entire digit Eg 435.

    Example:
        Original: The maximum of 311, 342, 435, 237, 218 is 435.
        Masked: The maximum of 311, 342, <extra_id_0>, 237, 218 is 435.

    Args:
        sentence: A sentence to be masked.
    Returns:
        List of samples, such that each sample contains
            sent: A masked sentence.
            targets: The masked part(s) of the input.
    """
    samples = []

    # Find all matches using Regex
    pattern = re.compile(r"\d+")
    for match in pattern.finditer(sentence):
        # Extract match
        start, end = match.span()
        text = match.group()

        # Replace match with mask token
        masked = sentence[:start] + config.MASK_TOKEN.format(0) + sentence[end:]
        label = config.MASK_TOKEN.format(0) + " " + text + " " + config.MASK_TOKEN.format(1)

        # Append sample
        yield Sample(sent=masked, label=label)

def mask_multiple_numbers(sentence: str) -> Generator[Sample, None, None]:
    """Masks the multiple digits.

    Example:
        Original: The maximum of 311, 342, 435, 237, 218 is 435.
        Masked: The maximum of 311, 342, <extra_id_0>, 237, <extra_id_1> is 435.

    Args:
        sentence: A sentence to be masked.
    Returns:
        List of samples, such that each sample contains
            sent: A masked sentence.
            targets: The masked part(s) of the input.
    """
    samples = []

    # Find all matches using Regex
    pattern = re.compile(r"\d+")
    for match in pattern.finditer(sentence):
        start, end = match.span()
        text_one = match.group()
        # Replace match with mask token
        masked_one = sentence[:start] + config.MASK_TOKEN.format(0) + sentence[end:0]
        newSentence = sentence[end:]
        for match in pattern.finditer(newSentence):
            start, end = match.span()
            text_two = match.group()
            # Replace match with mask token
            masked = masked_one + newSentence[:start] + config.MASK_TOKEN.format(1) + newSentence[end:]
            label = config.MASK_TOKEN.format(0) + " " + text_one + " " + config.MASK_TOKEN.format(1) + " " +  text_two + " " + config.MASK_TOKEN.format(2)

        # Append sample
        yield Sample(sent=masked, label=label)


masks = {
    'mask_one_digit': mask_one_digit,
    'mask_one_number': mask_one_number,
    'mask_multiple_numbers':mask_multiple_numbers
}
