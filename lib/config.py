NUMS_VAL_RANGE = (0, 100)
NUMS_LEN_RANGE = (5, 10)
TASKS = {
    "minimum": min,
    "maximum": max,
}
DATASET_COLS = ["feature", "label"]
DATASET_PATH = "../data/raw/dataset.h5"
MASK_TOKEN = "<extra_id_{0}>"

SPLIT = {'train': 0.7, 'val': 0.1, 'test': 0.2}
