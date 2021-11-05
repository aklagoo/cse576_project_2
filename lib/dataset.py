"""This module contains dataset generation and loading functions.

The datasets are stored in a single HDF5 file for faster access. Both generation
functions write all data to a common file, such that each format-mask pair is
stored as a separate table, named with the format {sent_format}_{sent_mask}.
"""
from lib import config, formats, masks
import tables
from itertools import product
from tables.table import Table
from typing import List, NamedTuple, Union, Tuple, Dict


# Define data formats
class Sample(NamedTuple):
    sent: str
    label: str


class SampleTable(tables.IsDescription):
    sent = tables.StringCol(200)
    label = tables.StringCol(50)


def _combine_iter(combinations: List[List[int]], data: List[int]) -> List[List[int]]:
    """Returns a cartesian product of combinations and data."""
    combinations_ = []
    for combination in combinations:
        for x in data:
            nums = combination + [x]
            combinations_.append(nums)
    return combinations_


def _create_table(h5file, sent_format, sent_mask, rewrite):
    """Creates a table for a format-mask pair."""
    table_name = "{sent_format}_{sent_mask}".format(sent_format=sent_format, sent_mask=sent_mask)

    # Remove table if it exists
    if f"/datasets/{table_name}" in h5file:
        if not rewrite:
            raise KeyError("Table already exists")
        else:
            h5file.root.datasets[table_name].remove()

    # Create table
    table = h5file.create_table(h5file.root.datasets, table_name, SampleTable, table_name)
    return table


def generate_all(
        path: str = config.DATASET_PATH, rewrite: bool = False,
        sent_formats: Union[str, List[str]] = 'all',
        sent_masks: Union[str, List[str]] = 'all'):
    """Generates and writes a dataset with all combinations.

    This method generates all possible combinations of numbers in a value range
    config.NUMS_VAL_RANGE and of a length between config.NUMS_LEN_RANGE. Each
    combination is then formatted into a sentence. This sentence has different
    parts masked to generate several masks.

    Example:
        Numbers: [1, 2, 3, 4]; Task: maximum
        Formatted sentence: The maximum among 1, 2, 3, and 4 is 4.
        Samples after masking:
            ("The maximum among <extra_id_0>, 2, 3, and 4 is 4.", "<extra_id_0> 1 <extra_id_1>"),
            ("The maximum among 1, <extra_id_0>, 3, and 4 is 4.", "<extra_id_0> 2 <extra_id_1>"),
            ...

    Args:
        path: Path to the dataset.
        rewrite: If set, existing tables are deleted and reinitialized.
        sent_formats: One or more sentence formats.
        sent_masks: One or more methods of masking.
    """
    # Check arguments
    if isinstance(sent_formats, str):
        if sent_formats == "all":
            sent_formats_ = formats.formats
        elif sent_formats in formats.formats:
            sent_formats_ = [sent_formats]
        else:
            raise KeyError(f"Format \"{sent_formats}\" does not exist.")
    elif isinstance(sent_formats, list):
        sent_formats_ = sent_formats
    else:
        raise TypeError(f"Invalid type for \"sent_formats\".")

    if isinstance(sent_masks, str):
        if sent_masks == "all":
            sent_masks_ = masks.masks
        elif sent_masks in masks.masks:
            sent_masks_ = [sent_masks]
        else:
            raise KeyError(f"Mask \"{sent_masks}\" does not exist.")
    elif isinstance(sent_masks, list):
        sent_masks_ = sent_masks
    else:
        raise TypeError(f"Invalid type for \"sent_masks\".")

    # Open or create dataset file
    with tables.open_file(path, mode="a", title="Datasets") as h5file:
        # Create a group if it doesn't exist
        if '/datasets' not in h5file:
            h5file.create_group('/', 'datasets', 'Datasets')

        # Generate all task-format-mask pairs
        for task_name, sent_format, sent_mask in product(
                config.TASKS.keys(), sent_formats_, sent_masks_):
            # Create a new table
            table = _create_table(h5file, sent_format, sent_mask, rewrite)
            row = table.row

            # Generate examples
            start, end = config.NUMS_LEN_RANGE
            data = list(range(*config.NUMS_VAL_RANGE))
            combinations = list(map(lambda x: [x], data))

            # Create initial data
            for i in range(start - 2):
                combinations = _combine_iter(combinations, data)

            # Generate tasks for combinations
            for _ in range(start, end + 1):
                combinations = _combine_iter(combinations, data)

                # For each combination, generate all samples
                for combination in combinations:
                    # Generate samples for combination
                    target = config.TASKS[task_name](combination)
                    sentence = formats.formats[sent_format](task_name, combination, target)
                    samples = masks.masks[sent_mask](sentence)

                    # Write samples to table
                    for sample in samples:
                        row['sent'] = sample.sent
                        row['label'] = sample.label
                        row.append()

        # Flush table
        table.flush()


def generate_random(
        count: int, path: str = config.DATASET_PATH, rewrite: bool = False,
        sent_formats: Union[str, List[str]] = 'all',
        sent_masks: Union[str, List[str]] = 'all'):
    # TODO Fill stub
    pass


def load_datasets(
        path: str = config.DATASET_PATH,
        sent_formats: Union[str, List[str]] = 'all',
        sent_masks: Union[str, List[str]] = 'all') -> Dict[str, Table]:
    # TODO Fill stub
    return {}
