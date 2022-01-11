import numpy as np
from random import randrange
import bingo.Utils as Utils
from bingo.Prize import Prize


class BaseCard:

    def __init__(self, card_numbers, is_bank=False, id_card=0, color=None):
        self.id_card = id_card
        self.is_bank = is_bank
        self.card_numbers = self.well_format_card_numbers(card_numbers) \
            if not is_bank else self.get_np_array_dict_numbers(card_numbers)
        self.extracted_by_row = np.zeros(3, dtype=np.int8)
        self.color = color

    def well_format_card_numbers(self, card_numbers):
        card_numbers = self.set_90_at_corner_if_present(card_numbers)
        full_columns_indexes = self.get_full_columns(card_numbers)
        exceed_numbers = [[] for _ in range(9)]

        for i in range(card_numbers.shape[0]):
            row = card_numbers[i, :]
            row_below = card_numbers[i+1, :] if i == 1 else np.zeros(9)

            exceed_last_row_intersection_indexes = [index for index, number in enumerate(row_below)
                                                    if number > 0 and exceed_numbers[index]]

            for index in exceed_last_row_intersection_indexes:
                row[index] = exceed_numbers[index].pop()

            not_zero_indexes = np.where(row > 0)[0]

            if len(not_zero_indexes) > 5:
                changeable_indexes = np.delete(not_zero_indexes, full_columns_indexes)
                already_stored_indexes = [index for index, value in enumerate(changeable_indexes)
                                          if exceed_numbers[value]]
                intersection_with_below = [index for index, value in enumerate(changeable_indexes) if row_below[value] > 0]

                changeable_indexes = np.delete(changeable_indexes, already_stored_indexes + intersection_with_below)
                n_col_to_keep = 5 - len(full_columns_indexes) - len(already_stored_indexes) - len(intersection_with_below)
                for _ in range(n_col_to_keep):
                    random_index = randrange(len(changeable_indexes))
                    changeable_indexes = np.delete(changeable_indexes, random_index)

                for j in changeable_indexes:
                    exceed_numbers[j].append(card_numbers[i][j])
                    card_numbers[i][j] = 0

            elif len(not_zero_indexes) < 5:
                zero_indexes = np.where(row == 0)[0]
                available_zero_indexes = [index for index in zero_indexes if exceed_numbers[index]]
                n_col_to_fill = 5 - len(not_zero_indexes)
                for _ in range(n_col_to_fill):
                    random_index = randrange(len(available_zero_indexes))
                    random_col_number = available_zero_indexes[random_index]
                    card_numbers[i][random_col_number] = exceed_numbers[random_col_number].pop()
                    available_zero_indexes = np.delete(available_zero_indexes, random_index)

        card_numbers_dict = self.get_np_array_dict_numbers(card_numbers)

        return card_numbers_dict

    def set_extracted_and_check_win(self, new_number, current_prize):
        """Sets number extracted and returns if is present and if card wins prize.
            After setting extracted_by_row is incremented and check for winner is done using this helper list.

            @type new_number: int
            @param new_number: number just extracted
            @type current_prize: int
            @param current_prize: number of checked values needed to win prize
            @rtype: tuple
            @returns: is present and is winner tuple
        """
        is_present = is_winner = False
        column_index = self.get_column_index(new_number, is_bank=self.is_bank)
        row = 0
        # check if number is present
        while not is_present and row < self.card_numbers.shape[0]:
            if str(new_number) in map(lambda c: str(c), self.card_numbers[row][column_index]):
                is_present = True
                self.card_numbers[row][column_index] = {str(new_number): True}
                self.extracted_by_row[row] += 1
            else:
                row += 1

        if is_present:
            if current_prize == Prize.TOMBOLA.value:
                extracted_numbers = sum(self.extracted_by_row)
            else:
                extracted_numbers = self.extracted_by_row[row]

            is_winner = extracted_numbers == current_prize

        return is_present, is_winner

    @staticmethod
    def get_np_array_dict_numbers(card_numbers):
        """Converts card numbers np.array of int in np.array of dict with extracted bool set first at False.

            @type card_numbers: np.array
            @param card_numbers: int matrix with cards number
            @rtype: np.array
            @returns: dict matrix with cards number and extracted False
        """
        card_numbers_size = card_numbers.shape
        return np.array(
            [[Utils.create_dict_num_and_extracted(card_numbers[row][col])
              for col in range(card_numbers_size[1])]
                for row in range(card_numbers_size[0])], dtype=dict)

    @staticmethod
    def get_full_columns(card_numbers):
        """Searches for columns of card with no available space (3 values in column)

            @type card_numbers: np.array
            @param card_numbers: int matrix with cards number
            @rtype: list
            @returns: list of full column indexes
        """
        full_columns_indexes = []
        for i in range(card_numbers.shape[1]):
            column = card_numbers[:, i]
            if len(column[column > 0]) == 3:
                full_columns_indexes.append(i)

        return full_columns_indexes

    @staticmethod
    def set_90_at_corner_if_present(card_numbers):
        """If 90 is present in card, set it to right bottom corner and swap position with number in that place

            @type card_numbers: np.array
            @param card_numbers: int matrix with cards number
            @rtype: np.array
            @returns: int matrix with cards number and 90 at right bottom corner if present
        """
        last_column = card_numbers[:, 8]
        if 90 in last_column:
            row_90 = np.where(last_column == 90)[0][0]
            old_value_corner = card_numbers[2, 8]
            card_numbers[2, 8] = 90
            card_numbers[row_90, 8] = old_value_corner
        return card_numbers

    @staticmethod
    def get_column_index(number, is_bank=False):
        """Gets column index based on number passed. For not bank cards, it depends on ten of number. For bank ones,
            it depends on unit digit.

            @type number: int
            @param number: number to check
            @type is_bank: bool
            @param is_bank: bank card or not (default is False)
            @rtype: int
            @returns: column index
        """
        if not is_bank:
            column_index = int(number / 10)
            return column_index - 1 if column_index == 9 else column_index
        else:
            unit_of_number = (number % 10) - 1
            if unit_of_number == -1:
                unit_of_number = 9
            return unit_of_number if unit_of_number <= 4 else unit_of_number - 5

    def __str__(self) -> str:
        card_str = f'card {self.id_card}: \n'
        for row in self.card_numbers:
            for num in row:
                if list(num.values())[0]:
                    card_str += '\033[4m' + str(list(num.keys())[0]) + '\033[0m  '
                else:
                    card_str += str(list(num.keys())[0]) + '  '

            card_str += '\n'
        return card_str
