import numpy as np
from random import randrange
import bingo.Utils as Utils


class BaseCard:

    def __init__(self, card_numbers, is_bank=False, id_card=0):
        self.id_card = id_card
        self.card_numbers = self.well_format_card_numbers(card_numbers) \
            if not is_bank else self.get_np_array_dict_numbers(card_numbers)

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

    @staticmethod
    def get_np_array_dict_numbers(card_numbers):
        card_numbers_size = card_numbers.shape
        return np.array(
            [[Utils.create_dict_num_and_extracted(card_numbers[row][col])
              for col in range(card_numbers_size[1])]
                for row in range(card_numbers_size[0])], dtype=dict)

    @staticmethod
    def get_full_columns(card_numbers):
        full_columns_indexes = []
        for i in range(card_numbers.shape[1]):
            column = card_numbers[:, i]
            if len(column[column > 0]) == 3:
                full_columns_indexes.append(i)

        return full_columns_indexes

    @staticmethod
    def set_90_at_corner_if_present(card_numbers):
        last_column = card_numbers[:, 8]
        if 90 in last_column:
            row_90 = np.where(last_column == 90)[0][0]
            old_value_corner = card_numbers[2, 8]
            card_numbers[2, 8] = 90
            card_numbers[row_90, 8] = old_value_corner
        return card_numbers

    def __str__(self) -> str:
        card_str = f'card {self.id_card}: \n'
        for row in self.card_numbers:
            card_str += str(row) + '\n'
        return card_str
