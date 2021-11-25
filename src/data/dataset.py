"""This module contains dataset generation and loading functions.

The datasets are stored in a single HDF5 file for faster access. Both generation
functions write all data to a common file, such that each format-mask pair is
stored as a separate table, named with the format {sent_format}_{sent_mask}.
"""
import random

from src.data import formats, masks
from src import config
import tables
from itertools import product
from tables.table import Table
from src.data.masks import Sample
from typing import List, Tuple, Union, Dict, Generator


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


def _create_tables(h5file, sent_format, sent_mask, rewrite) -> Dict[str, Table]:
    """Creates train-val-test tables for a format-mask pair."""
    group_name = "{sent_format}_{sent_mask}".format(sent_format=sent_format, sent_mask=sent_mask)

    # Remove group if it exists
    if group_name in h5file.root.datasets:
        if rewrite:
            h5file.remove_node("/datasets", group_name, recursive=True)
        else:
            raise tables.NodeError(f"Group {group_name} already exists")

    # Create group and tables
    h5file.create_group(f"/datasets", group_name, group_name)
    data_tables = {
        'train': h5file.create_table(h5file.root.datasets[group_name], 'train', SampleTable, 'train'),
        'val': h5file.create_table(h5file.root.datasets[group_name], 'val', SampleTable, 'val'),
        'test': h5file.create_table(h5file.root.datasets[group_name], 'test', SampleTable, 'test'),
    }
    return data_tables


def _get_row(data_tables, counts, split: Dict[str, float]):
    """Returns the row of the table that's lacking the most samples."""
    count_total = max(1, sum(counts.values()))
    caps = {table_type: split[table_type] * count_total - count for table_type, count in counts.items()}
    table_type = max(caps, key=caps.get)
    row = data_tables[table_type].row
    return row, table_type


def _parse_params(sent_formats: Union[str, List[str]], sent_masks: Union[str, List[str]]) -> (List[str], List[str]):
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
    return sent_formats_, sent_masks_


def _generate_samples_all(
        sent_format: str, sent_mask: str, task_name: str,
        val_range: Tuple[int, int], len_range: Tuple[int, int])\
        -> Generator[Sample, None, None]:
    # Generate examples
    start, end = len_range
    data = list(range(*val_range))
    combinations = list(map(lambda x: [x], data))

    # Create initial data
    for i in range(start - 2):
        combinations = _combine_iter(combinations, data)

    # Generate tasks for combinations
    for _ in range(start, end):
        combinations = _combine_iter(combinations, data)

        # For each combination, generate all samples
        for combination in combinations:
            # Generate samples for combination
            target = config.TASKS[task_name](combination)
            sentence = formats.formats[sent_format](task_name, combination, target)
            samples = masks.masks[sent_mask](sentence)

            # Write samples to table
            for sample in samples:
                yield sample


def generate_all(
        val_range: Tuple[int, int] = config.NUMS_VAL_RANGE,
        len_range: Tuple[int, int] = config.NUMS_LEN_RANGE,
        path: str = config.DATASET_PATH, rewrite: bool = False,
        sent_formats: Union[str, List[str]] = 'all',
        sent_masks: Union[str, List[str]] = 'all',
        split: Dict[str, float] = config.SPLIT):
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
        val_range: Tuple [start, end) representing the range of values.
        len_range: Tuple [start, end) representing the range of sample lengths.
        path: Path to the dataset.
        rewrite: If set, existing tables are deleted and reinitialized.
        sent_formats: One or more sentence formats.
        sent_masks: One or more methods of masking.
        split: A train-val-test split ratio.
    """
    # Check arguments
    sent_formats_, sent_masks_ = _parse_params(sent_formats, sent_masks)

    # Open or create dataset file
    with tables.open_file(path, mode="a", title="Datasets") as h5file:
        # Create a group if it doesn't exist
        if '/datasets' not in h5file:
            h5file.create_group('/', 'datasets', 'Datasets')

        # Generate all task-format-mask pairs
        for sent_format, sent_mask in product(sent_formats_, sent_masks_):
            # Initialize counts
            counts = {'train': 0, 'val': 0, 'test': 0}

            # Create train-val-test tables
            data_tables = _create_tables(h5file, sent_format, sent_mask, rewrite)
            for task_name in config.TASKS.keys():
                for sample in _generate_samples_all(sent_format, sent_mask, task_name, val_range, len_range):
                    # Pick row and append a sample
                    row, table_type = _get_row(data_tables, counts, split)
                    row['sent'] = sample.sent
                    row['label'] = sample.label
                    row.append()
                    counts[table_type] += 1

        # Flush tables
        for table in data_tables.values():
            table.flush()


def _generate_samples_random(
        count: int, sent_format: str, sent_mask: str, task_name: str,
        val_range: Tuple[int, int], len_range: Tuple[int, int])\
        -> Generator[Sample, None, None]:
    for _ in range(count):
        # Generate random length
        nums_l = random.randrange(*len_range)
        nums = [random.randrange(*val_range) for _ in range(nums_l)]

        # Generate samples for combination
        target = config.TASKS[task_name](nums)
        sentence = formats.formats[sent_format](task_name, nums, target)
        samples = masks.masks[sent_mask](sentence)

        # Yield a single sample
        yield random.choice(list(samples))


def generate_random(
        count: int, val_range: Tuple[int, int] = config.NUMS_VAL_RANGE,
        len_range: Tuple[int, int] = config.NUMS_LEN_RANGE,
        path: str = config.DATASET_PATH, rewrite: bool = False,
        sent_formats: Union[str, List[str]] = 'all',
        sent_masks: Union[str, List[str]] = 'all',
        split: Dict[str, float] = config.SPLIT):
    """Generates and writes a dataset with random samples.

    The samples generated have values similar to generate_all, except for the
    random generation.

    Args:
        count: The number of samples.
        val_range: Tuple [start, end) representing the range of values.
        len_range: Tuple [start, end) representing the range of sample lengths.
        path: Path to the dataset.
        rewrite: If set, existing tables are deleted and reinitialized.
        sent_formats: One or more sentence formats.
        sent_masks: One or more methods of masking.
        split: A train-val-test split ratio.
    """
    # Parse arguments
    sent_formats_, sent_masks_ = _parse_params(sent_formats, sent_masks)

    # Open or create dataset file
    with tables.open_file(path, mode="a", title="Datasets") as h5file:
        # Create a group if it doesn't exist
        if '/datasets' not in h5file:
            h5file.create_group('/', 'datasets', 'Datasets')

        # Generate all task-format-mask pairs
        for sent_format, sent_mask in product(
                sent_formats_, sent_masks_):
            # Initialize counts
            counts = {'train': 0, 'val': 0, 'test': 0}

            # Create train-val-test tables
            data_tables = _create_tables(h5file, sent_format, sent_mask, rewrite)
            for task_name in config.TASKS.keys():
                for sample in _generate_samples_random(count, sent_format, sent_mask, task_name, val_range, len_range):
                    # Pick row and append a sample
                    row, table_type = _get_row(data_tables, counts, split)
                    row['sent'] = sample.sent
                    row['label'] = sample.label
                    row.append()
                    counts[table_type] += 1

        # Flush tables
        for table in data_tables.values():
            table.flush()


def load_datasets(
        path: str = config.DATASET_PATH,
        sent_formats: Union[str, List[str]] = 'all',
        sent_masks: Union[str, List[str]] = 'all') -> (tables.File, Dict[str, Table]):
    # Load file
    h5file = tables.open_file(path, mode="r")

    # Return tables
    datasets = {}
    sent_formats_, sent_masks_ = _parse_params(sent_formats, sent_masks)
    for sent_format, sent_mask in product(sent_formats_, sent_masks_):
        group_name = "{sent_format}_{sent_mask}".format(sent_format=sent_format, sent_mask=sent_mask)
        datasets[sent_format][sent_mask] = h5file.root.datasets[group_name]

    return h5file, datasets
