from bingo.Utils import PAPER_NUMBERS
from random import choice
import numpy as np
from bingo.Utils import np_pop
from bingo.base_model.BaseCard import BaseCard
from bingo.Card import Card
from bingo.Utils import db


class BaseBingoPaper:

    def __init__(self, color=None, is_bank=False, id_paper=0):
        self.paper_cards_numbers = PAPER_NUMBERS
        self.id_paper = id_paper
        self.cards = self.generate_cards(is_bank, color=color)

    def generate_cards(self, is_bank=False, color=None):  # Each bingo paper must contain number from 1 to 90 without repetitions
        cards = []
        cards_numbers = self.generate_cards_numbers() if not is_bank else self.generate_bank_cards_numbers()
        for i, card_numbers in enumerate(cards_numbers):
            id_card = (i + self.id_paper * 6) + 1
            cards.append(BaseCard(card_numbers, is_bank=is_bank, id_card=id_card, color=color))
        return cards

    def generate_cards_numbers(self):
        cards = []
        for _ in range(6):  # Filled one number per unit in each card
            card = np.zeros((3, 9), dtype=int)
            self.set_number_per_unit(card)
            cards.append(card)

        while len(self.paper_cards_numbers) > 0:
            number, self.paper_cards_numbers = np_pop(self.paper_cards_numbers)
            column_index = BaseCard.get_column_index(number)

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

    @staticmethod
    def generate_bank_cards_numbers():
        cards = []
        for first_left_number in range(1, 91, 30):
            card_left = np.array(
                [[num + 10 * prod_10_factor
                  for num in range(first_left_number, first_left_number + 5)]
                    for prod_10_factor in range(3)], dtype=int)
            card_right = np.array(
                [[num + 10 * prod_10_factor
                  for num in range(first_left_number + 5, first_left_number + 10)]
                 for prod_10_factor in range(3)], dtype=int)
            cards.append(card_left)
            cards.append(card_right)
        return cards

    def set_number_per_unit(self, card):
        for i in range(9):
            possible_indexes_for_range = self.get_indexes_in_range_unit(i)
            random_index = choice(possible_indexes_for_range)
            card[0, i] = self.paper_cards_numbers[random_index]
            self.paper_cards_numbers = np.delete(self.paper_cards_numbers, random_index)

    def get_cards_with_number_and_winner(self, new_number, current_prize):
        cards_and_winner = dict()
        for card in self.cards:
            is_present, is_winner = card.set_extracted_and_check_win(new_number, current_prize)
            if is_present:
                if isinstance(card, Card):
                    cards_and_winner[card.id] = is_winner
                elif isinstance(card, BaseCard):
                    cards_and_winner[card.id_card] = is_winner
        return cards_and_winner

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
    def get_cards_with_available_column(all_cards, column_index, check_total_numbers=True):
        available_cards = []
        for card in all_cards:
            total_numbers = np.count_nonzero(card)
            column = card[:, column_index]
            numbers_in_column = len(column[column > 0])
            if (total_numbers < 15 or not check_total_numbers) and (
                    total_numbers == 15 or check_total_numbers) and numbers_in_column < 3:
                first_available_index = np.where(column == 0)[0][0]
                available_cards.append((card, first_available_index))
        return available_cards

    @staticmethod
    def get_random_number_from_second_third_rows(card):
        temp_card = np.zeros((2, 9))
        for i in range(1, 3):
            temp_card[i - 1, :] = card[i, :]
        return choice(temp_card[temp_card > 0])
