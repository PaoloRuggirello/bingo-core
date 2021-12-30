from bingo.Utils import db
from bingo.base_model.BaseCard import BaseCard


class Card(db.Model, BaseCard):
    id = db.Column('id', db.Integer, primary_key=True)
    card_numbers = db.Column('card_numbers', db.String(200), nullable=True)
    paper_id = db.Column('paper_id', db.Integer, db.ForeignKey('bingo_paper.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))

    def __init__(self, card_numbers, is_bank=False):
        super().__init__(card_numbers, is_bank)


