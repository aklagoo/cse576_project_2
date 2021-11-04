NUMS_VAL_RANGE = (0, 100)
NUMS_LEN_RANGE = (5, 10)
TASKS = {
    "minimum": min,
    "maximum": max,
}
DATASET_COLS = ["feature", "label"]
DATASET_PATH = "../data/raw/dataset.hdf5"
SENT_FORMATS = [
    "The {task} value among {nums_str} is {nums_target}.",
]
