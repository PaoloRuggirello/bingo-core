from bingo.Card import Card

class BingoPaper:

    def __init__(self):
        self.cards = self.generate_cards()

    def generate_cards(self): # Each bingo paper must contain number from 1 to 90 without repetitions
        cards = []
        for i in range(1, 7):
            cards.append(Card(i))
        return cards
