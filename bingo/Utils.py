import numpy as np

PAPER_NUMBERS = np.arange(90) + 1


def np_pop(np_array):
    number = np_array[0]
    np_array = np.delete(np_array, 0)
    return number, np_array
