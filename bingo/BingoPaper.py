from bingo.Utils import db, generate_random_hex_color
from sqlalchemy.orm import relationship
from bingo.base_model.BaseBingoPaper import BaseBingoPaper
from bingo.Card import Card


class BingoPaper(db.Model, BaseBingoPaper):
    """
    This class describe the model of the bingo paper that is the main entity which contains 6 different cards with
    numbers from 1 to 90
    """

    # The following rows are useful to tell to the orm how the BingoPaper fields must be stored in db
    id = db.Column('id', db.Integer, primary_key=True)
    is_host = db.Column('is_host', db.Boolean, default=False)
    room_id = db.Column('room_id', db.Integer, db.ForeignKey('room.id'))
    cards = relationship("Card")
    color = db.Column('color', db.String(10))

    def __init__(self, room_id, is_bank=False):
        self.color = generate_random_hex_color()
        BaseBingoPaper.__init__(self, color=self.color, is_bank=is_bank)
        self.room_id = room_id
        self.is_host = is_bank

    def generate_cards(self, is_bank=False, color=None):  # Each bingo paper must contain number from 1 to 90 without repetitions
        cards = []
        cards_numbers = self.generate_cards_numbers() if not is_bank else self.generate_bank_cards_numbers()
        for card_numbers in cards_numbers:
            cards.append(Card(card_numbers, is_bank=is_bank, color=color))
        return cards
