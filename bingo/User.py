from sqlalchemy.orm import relationship
from bingo.Utils import db
from bingo.base_model.BaseUser import BaseUser


class User(db.Model, BaseUser):
    """
    This class describe the user entity
    """

    # The following rows are useful to tell to the orm how the User fields must be stored in db
    id = db.Column('id', db.Integer, primary_key=True)
    nickname = db.Column('nickname', db.String(20))
    room_id = db.Column('room_id', db.ForeignKey('room.id'))
    cards = relationship("Card")

    def __init__(self, nickname, room_id):
        BaseUser.__init__(self, nickname)
        self.room_id = room_id
