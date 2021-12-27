from bingo.Card import Card
from bingo.Utils import PAPER_NUBERS
from random import randrange, choice
import numpy as np


class BingoPaper:

    def __init__(self):
        self.paper_cards_numbers = PAPER_NUBERS
        self.cards = self.generate_cards()

    def generate_cards(self):  # Each bingo paper must contain number from 1 to 90 without repetitions
        cards = []
        for i in range(1, 7):
            card_numbers = self.get_card_numbers()
            cards.append(Card(i, card_numbers))
        return cards

    def get_card_numbers(self):
        card_columns = [[] for _ in range(9)]  # Creating empty array of 9 empty arrays
        for i in range(9):
            random_index = choice(self.get_indexes_in_range_unit(i))
            card_columns[i].append(self.paper_cards_numbers[random_index])
            self.paper_cards_numbers = np.delete(self.paper_cards_numbers, random_index)

        i = 0
        while i < 6:  # Each card has 15 numbers
            random_index = randrange(self.paper_cards_numbers.size)
            column_index = self.get_column_index(random_index)
            if len(card_columns[column_index]) < 3:
                card_columns[column_index].append(self.paper_cards_numbers[random_index])
                self.paper_cards_numbers = np.delete(self.paper_cards_numbers, random_index)
                i += 1
        return card_columns

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


