from bingo.Utils import db
from bingo.base_model.BaseCard import BaseCard
from bingo.NPArray import NPArray
import numpy as np


class Card(db.Model, BaseCard):
    id = db.Column('id', db.Integer, primary_key=True)
    card_numbers = db.Column('card_numbers', NPArray(), nullable=True)
    paper_id = db.Column('paper_id', db.Integer, db.ForeignKey('bingo_paper.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    extracted_by_row = db.Column('extracted_by_row', NPArray())
    is_bank = db.Column('is_bank', db.Boolean, default=False)

    def __init__(self, card_numbers, is_bank=False):
        BaseCard.__init__(self, card_numbers, is_bank)
        self.extracted_by_row = np.zeros(3)


