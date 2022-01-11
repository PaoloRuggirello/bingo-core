import numpy as np
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from math import ceil
import random, string, argparse
from bingo.Prize import Prize
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bingo:bingo@database/bingo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'ChangeThisKey'  # TODO: Change the key
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)

PAPER_NUMBERS = np.arange(90) + 1
PRIZE_LIST = Prize.list()
users_subscriptions = {}


def np_pop(np_array):
    """Pops the first value of a numpy array

        @type np_array: np.array
        @param np_array: not empty numpy array
        @rtype: tuple
        @returns: number popped and list without value
    """
    number = np_array[0]
    np_array = np.delete(np_array, 0)
    return number, np_array


def np_pop_random(np_array):
    """Pops the random value from a numpy array

        @type np_array: np.array
        @param np_array: not empty numpy array
        @rtype: tuple
        @returns: number popped and list without value
        """
    random_index = random.randrange(0, len(np_array))
    number = np_array[random_index]
    np_array = np.delete(np_array, random_index)
    return number, np_array


def initialize_parser():
    """Utility method that initializes argparse and return the args

        @rtype: Namespace object
        @returns: object built up from attributes parsed out of the command line
    """
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
    """Return the number of bingo papers needed to satisfy the requests

        @type total_number_cards: int
        @param total_number_cards: total number of cards requested
        @rtype: int
        @returns: number of bingo paper needed
    """
    return ceil(total_number_cards / 6)


def get_random_room_code(k=5):
    """Return a random room code for the room created

        @type k: int
        @param k: number of characters (default is 5)
        @rtype: str
        @returns: k characters random room code
    """
    random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=k)).upper()
    return random_code


def create_dict_num_and_extracted(number) -> dict:
    """Return the default dict with extracted (value of dict) set as False

        @type number: int
        @param number: number of card
        @rtype: dict
        @returns: dict with key=number and value=False
    """
    return {int(number): False}


def generate_random_hex_color():
    """Return a random color in hex format

        @rtype: str
        @returns: hex string random color
    """
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
