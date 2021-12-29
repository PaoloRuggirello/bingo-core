import numpy as np
from math import ceil
import argparse

PAPER_NUMBERS = np.arange(90) + 1


def np_pop(np_array):
    number = np_array[0]
    np_array = np.delete(np_array, 0)
    return number, np_array


def initialize_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gamers",
                        help="Number of gamers for bingo",
                        required=True,
                        type=str,)
    parser.add_argument("-n", "--number_of_cards",
                        help="Number of cards for each player",
                        type=str,
                        required=True,
                        nargs='+')
    return parser.parse_args()


def get_number_of_papers_needed(total_number_cards) -> int:
    # one is for bank
    return ceil(total_number_cards / 6)
