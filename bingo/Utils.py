import numpy as np
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from math import ceil
import random, string, argparse
from bingo.Prize import Prize
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysql:mysql@localhost/bingo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'ChangeThisKey'  # TODO: Change the key
db = SQLAlchemy(app)
socketio = SocketIO(app)
CORS(app)

PAPER_NUMBERS = np.arange(90) + 1
PRIZE_LIST = Prize.list()
users_subscriptions = {}



def np_pop(np_array):
    number = np_array[0]
    np_array = np.delete(np_array, 0)
    return number, np_array


def np_pop_random(np_array):
    random_index = random.randrange(0, len(np_array))
    number = np_array[random_index]
    np_array = np.delete(np_array, random_index)
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


def get_random_room_code(k=5):
    random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=k)).upper()
    return random_code


def create_dict_num_and_extracted(number) -> dict:
    return {int(number): False}


def generate_random_hex_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))