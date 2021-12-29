import numpy as np
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random, string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@localhost/bingo_db'
db = SQLAlchemy(app)

PAPER_NUMBERS = np.arange(90) + 1


def np_pop(np_array):
    number = np_array[0]
    np_array = np.delete(np_array, 0)
    return number, np_array


def get_random_room_code():
    random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=5)).upper()
    return random_code

