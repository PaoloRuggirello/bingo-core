from bingo.BingoPaper import BingoPaper


if __name__ == '__main__':
    print("Bingo-core online")
    bingo_paper = BingoPaper()
    for card in bingo_paper.cards:
        print(card)