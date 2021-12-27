import numpy as np
from random import randrange


class Card:

    def __init__(self, number, card_columns):
        self.number = number
        self.rows = np.zeros((3, 9), dtype=int)
        self.set_columns_values(card_columns)

    def set_columns_values(self, card_columns):
        for column_index, column in enumerate(card_columns):
            available_indexes = np.arange(self.rows.shape[0])
            for number_index, number in enumerate(column):
                random_index = randrange(len(available_indexes))
                self.rows[available_indexes[random_index]][column_index] = number
                del card_columns[column_index][number_index]
                available_indexes = np.delete(available_indexes, random_index)

    def __str__(self) -> str:
        card_str = f'card {self.number}: \n'
        for row in self.rows:
            card_str += str(row) + '\n'
        return card_str
