import numpy as np

from bingo.Utils import db, get_random_room_code
from sqlalchemy.orm import relationship
from bingo.NPArray import NPArray


class Room(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column('code', db.String(5), unique=True)
    name = db.Column('name', db.String(20))
    extracted_numbers = db.Column('extracted_numbers', NPArray, nullable=True)
    unique_code = db.Column('unique_code', db.String(6))
    papers = relationship("BingoPaper")
    users = relationship("User")

    def __init__(self, name, unique_code):
        self.name = name
        self.code = get_random_room_code()
        self.unique_code = unique_code
        self.extracted_numbers = np.empty(shape=0, dtype=int)
