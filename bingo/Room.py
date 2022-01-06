from bingo.Utils import db, get_random_room_code
from sqlalchemy.orm import relationship
from bingo.NPArray import NPArray
from bingo.DictInDB import DictInDB

class Room(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column('code', db.String(5), unique=True)
    name = db.Column('name', db.String(20))
    extracted_numbers = db.Column('extracted_numbers', NPArray(), nullable=True)
    current_prize_index = db.Column('current_prize_index', db.Integer)
    unique_code = db.Column('unique_code', db.String(6))
    papers = relationship('BingoPaper')
    users = relationship('User')
    winners = db.Column('winners', DictInDB())
    last_extracted_number = db.Column('last_extracted_number', db.Integer)

    def __init__(self, name, unique_code):
        self.name = name
        self.code = get_random_room_code()
        self.unique_code = unique_code
        self.current_prize_index = 0
        self.winners = {}
