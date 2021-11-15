"""This module is a command-line script for all functions."""
import argparse
from src.data import dataset
from src import config


def run_gen_all(x):
    # Parse sent_formats and sent_masks
    if x.sent_formats[0] == 'all':
        x.sent_formats = 'all'
    if x.sent_masks[0] == 'all':
        x.sent_masks = 'all'

    # Parse split
    split = {
        'train': x.split[0],
        'val': x.split[1],
        'test': x.split[2],
    }
    dataset.generate_all(
        val_range=x.val_range, len_range=x.len_range, path=x.path,
        rewrite=config.DATASET_REWRITE, sent_formats=x.sent_formats,
        sent_masks=x.sent_masks, split=split)


def run_gen_random(x):
    # Parse sent_formats and sent_masks
    if x.sent_formats[0] == 'all':
        x.sent_formats = 'all'
    if x.sent_masks[0] == 'all':
        x.sent_masks = 'all'

    # Parse split
    split = {
        'train': x.split[0],
        'val': x.split[1],
        'test': x.split[2],
    }
    dataset.generate_random(
        count=x.count[0], val_range=x.val_range, len_range=x.len_range,
        path=x.path, rewrite=config.DATASET_REWRITE,
        sent_formats=x.sent_formats, sent_masks=x.sent_masks, split=split)


def setup_parsers():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda arguments: parser.print_help())
    subparsers = parser.add_subparsers(help='Run commands for dataset generation, training and testing.')

    # Add sub-commands
    cmd_gen = subparsers.add_parser('generate_dataset')
    cmd_gen.set_defaults(func=lambda arguments: cmd_gen.print_help())
    cmd_gen_types = cmd_gen.add_subparsers(help='Types of datasets')

    # Add options for generate_all
    cmd_gen_all = cmd_gen_types.add_parser('all')
    cmd_gen_all.set_defaults(func=run_gen_all)
    cmd_gen_all.add_argument('--val_range', nargs=2, type=int, default=config.NUMS_VAL_RANGE)
    cmd_gen_all.add_argument('--len_range', nargs=2, type=int, default=config.NUMS_LEN_RANGE)
    cmd_gen_all.add_argument('--path', nargs=1, type=str, default=config.DATASET_PATH)
    cmd_gen_all.add_argument('--sent_formats', nargs='*', type=str, default='all')
    cmd_gen_all.add_argument('--sent_masks', nargs='*', type=str, default='all')
    cmd_gen_all.add_argument('--split', nargs=3, type=int, default=(config.SPLIT['train'], config.SPLIT['val'], config.SPLIT['test']))

    # Add options for generate_random
    cmd_gen_all = cmd_gen_types.add_parser('random')
    cmd_gen_all.set_defaults(func=run_gen_random)
    cmd_gen_all.add_argument('count', nargs=1, type=int)
    cmd_gen_all.add_argument('--val_range', nargs=2, type=int, default=config.NUMS_VAL_RANGE)
    cmd_gen_all.add_argument('--len_range', nargs=2, type=int, default=config.NUMS_LEN_RANGE)
    cmd_gen_all.add_argument('--path', nargs=1, type=str, default=config.DATASET_PATH)
    cmd_gen_all.add_argument('--sent_formats', nargs='*', type=str, default='all')
    cmd_gen_all.add_argument('--sent_masks', nargs='*', type=str, default='all')
    cmd_gen_all.add_argument('--split', nargs=3, type=int, default=(config.SPLIT['train'], config.SPLIT['val'], config.SPLIT['test']))

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    setup_parsers()
