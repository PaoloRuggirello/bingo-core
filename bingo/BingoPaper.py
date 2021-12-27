from bingo.Card import Card
from bingo.Utils import PAPER_NUMBERS
from random import randrange, choice
import numpy as np


class BingoPaper:

    def __init__(self):
        self.paper_cards_numbers = PAPER_NUMBERS
        self.cards = self.generate_cards()

    def generate_cards(self):  # Each bingo paper must contain number from 1 to 90 without repetitions
        cards = []
        for i in range(1, 7):
            card_numbers = self.get_card_numbers(missing_cards=6-i)
            cards.append(Card(i, card_numbers))
        return cards

    def get_card_numbers(self, missing_cards):
        card = np.zeros((3, 9), dtype=int)
        for i in range(9):
            possible_indexes_for_range = self.get_indexes_in_range_unit(i)
            random_index = choice(possible_indexes_for_range)
            card[0, i] = self.paper_cards_numbers[random_index]
            self.paper_cards_numbers = np.delete(self.paper_cards_numbers, random_index)

        i = 0
        while i < 6:  # Each card has 15 numbers
            random_index = randrange(self.paper_cards_numbers.size)
            column_index = self.get_column_index(random_index)
            if len(self.get_indexes_in_range_unit(column_index)) > missing_cards:
                column = card[:, column_index]
                numbers_in_column = len(column[column > 0])
                if numbers_in_column < 3:
                    card[numbers_in_column, column_index] = self.paper_cards_numbers[random_index]
                    self.paper_cards_numbers = np.delete(self.paper_cards_numbers, random_index)
                    i += 1

        return card

    def get_column_index(self, random_index):
        column_index = int(self.paper_cards_numbers[random_index] / 10)
        column_index = column_index - 1 if column_index == 9 else column_index
        return column_index

    def get_indexes_in_range_unit(self, range_unit):
        indexes = []
        for number_index, number in enumerate(self.paper_cards_numbers):
            if range_unit < 8:
                if int(number/10) == range_unit:
                    indexes.append(number_index)
            else:
                if int(number/10) == range_unit or int(number/10) == range_unit + 1:
                    indexes.append(number_index)
        return indexes


