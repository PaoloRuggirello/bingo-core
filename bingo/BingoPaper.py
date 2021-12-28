from bingo.Card import Card
from bingo.Utils import PAPER_NUMBERS
from random import choice
import numpy as np
from bingo.Utils import np_pop


class BingoPaper:

    def __init__(self):
        self.paper_cards_numbers = PAPER_NUMBERS
        self.cards = self.generate_cards()

    def generate_cards(self):  # Each bingo paper must contain number from 1 to 90 without repetitions
        cards = []
        for card_id, card_numbers in enumerate(self.generate_cards_numbers()):
            cards.append(Card(card_id + 1, card_numbers))
        return cards

    def generate_cards_numbers(self):
        cards = []
        for _ in range(6):  # Filled one number per unit in each card
            card = np.zeros((3, 9), dtype=int)
            self.set_number_per_unit(card)
            cards.append(card)

        while len(self.paper_cards_numbers) > 0:
            number, self.paper_cards_numbers = np_pop(self.paper_cards_numbers)
            column_index = self.get_column_index(number)

            # Wants to know which cards can store the number
            available_cards = self.get_cards_with_available_column(cards, column_index)
            if available_cards:
                chosen_card_tuple = choice(available_cards)  # Chosen_card is a tuple
            else:
                available_cards = self.get_cards_with_available_column(cards, column_index, False)
                chosen_card_tuple = choice(available_cards)
                random_number = int(self.get_random_number_from_second_third_rows(chosen_card_tuple[0]))
                self.paper_cards_numbers = np.append(self.paper_cards_numbers, random_number)
                chosen_card_tuple[0][chosen_card_tuple[0] == random_number] = 0

            chosen_card = chosen_card_tuple[0]
            chosen_card_free_index = chosen_card_tuple[1]

            chosen_card[chosen_card_free_index, column_index] = number

        return cards

    def set_number_per_unit(self, card):
        for i in range(9):
            possible_indexes_for_range = self.get_indexes_in_range_unit(i)
            random_index = choice(possible_indexes_for_range)
            card[0, i] = self.paper_cards_numbers[random_index]
            self.paper_cards_numbers = np.delete(self.paper_cards_numbers, random_index)

    def get_indexes_in_range_unit(self, range_unit):
        indexes = []
        for number_index, number in enumerate(self.paper_cards_numbers):
            if range_unit < 8:
                if int(number / 10) == range_unit:
                    indexes.append(number_index)
            else:
                if int(number / 10) == range_unit or int(number / 10) == range_unit + 1:
                    indexes.append(number_index)
        return indexes

    @staticmethod
    def get_column_index(number):
        column_index = int(number / 10)
        column_index = column_index - 1 if column_index == 9 else column_index
        return column_index

    @staticmethod
    def get_cards_with_available_column(all_cards, column_index, check_total_numbers=True):
        available_cards = []
        for card in all_cards:
            total_numbers = np.count_nonzero(card)
            column = card[:, column_index]
            numbers_in_column = len(column[column > 0])  # Equals to first available row index
            if (total_numbers < 15 or not check_total_numbers) and numbers_in_column < 3:
                available_cards.append((card, numbers_in_column))
        return available_cards

    @staticmethod
    def get_random_number_from_second_third_rows(card):
        temp_card = np.zeros((2, 9))
        for i in range(1, 3):
            temp_card[i-1, :] = card[i, :]
        return choice(temp_card[temp_card > 0])

