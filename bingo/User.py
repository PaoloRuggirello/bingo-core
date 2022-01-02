from sqlalchemy.orm import relationship
from bingo.Utils import db
from bingo.base_model.BaseUser import BaseUser


class User(db.Model, BaseUser):
    id = db.Column('id', db.Integer, primary_key=True)
    nickname = db.Column('nickname', db.String(20))
    room_id = db.Column('room_id', db.ForeignKey('room.id'))
    cards = relationship("Card")

    def __init__(self, nickname, room_id):
        super(BaseUser, self).__init__(nickname)
        self.room_id = room_id
