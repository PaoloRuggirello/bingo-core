import numpy as np


class Card:

    def __init__(self, number):
        self.number = number
        self.rows = np.zeros((3, 9), dtype=int)

    def __str__(self) -> str:
        card_str = f'card {self.number}: \n'
        for row in self.rows:
           card_str += str(row) + '\n'
        return card_str



