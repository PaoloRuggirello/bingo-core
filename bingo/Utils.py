import numpy as np
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from math import ceil
import random, string, argparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@localhost/bingo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

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
    return ceil(total_number_cards / 6)


def get_random_room_code():
    random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=5)).upper()
    return random_code


def create_dict_num_and_extracted(number) -> dict:
    return {number: False}
