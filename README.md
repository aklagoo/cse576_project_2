# Out-of-Order Generalization of Min/Max Operations
### Description
The project aims to train generalized models that work on out-of-order datasets.
The task is simple: pick the largest/smallest number from a list of numbers. 
Let's say the sentence is as follows:

The maximum value amongst 1, 2, and 3 is ____.

The model must be able to fill in the value, regardless of whether it has been trained on a similar problem.

### Current features
- Dataset generation
  - Random data
  - All combinations
  - Exporting dataset as an HDF5 file
  - Loading an HDF5 file
- A single sentence and mask with support for flexible addition 

### Installation
Run all the required libraries from `requirements.txt`.

```bash
pip install -r requirements.txt
```