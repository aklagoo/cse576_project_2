"""This module contains functions for sentence masking.

A masking function masks parts of an input sentence as defined in
"""
import re
from lib import config
from typing import Generator, NamedTuple


class Sample(NamedTuple):
    sent: str
    label: str


def mask_1d(sentence: str) -> Generator[Sample, None, None]:
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


masks = {
    '1d': mask_1d,
}
