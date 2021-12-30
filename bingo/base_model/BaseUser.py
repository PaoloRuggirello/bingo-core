class BaseUser:

    def __init__(self, nickname, cards=None):
        if cards is None:
            cards = []
        self.nickname = nickname
        self.user_cards = cards
