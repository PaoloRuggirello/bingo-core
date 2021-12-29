from bingo import Utils
from bingo.BingoPaper import BingoPaper

if __name__ == '__main__':
    print("Bingo-core online")
    GAMERS = None
    N_CARDS = None
    args = Utils.initialize_parser()
    try:
        GAMERS = int(args.gamers)
        N_CARDS = [int(n_cards) for n_cards in args.number_of_cards]
        if GAMERS != len(N_CARDS):
            print(f"Number of gamers ({GAMERS}) doesn't"
                  f' match length of number of cards ({len(N_CARDS)})')
            exit()
    except ValueError as e:
        print(e)
        exit()

    number_of_papers_for_gamers = Utils.get_number_of_papers_needed(sum(N_CARDS))
    bingo_papers = [BingoPaper(is_bank=True)]

    for _ in range(number_of_papers_for_gamers):
        bingo_papers.append(BingoPaper())

    for index, bingo_paper in enumerate(bingo_papers):
        if index == 0:
            print("Bank paper")
        else:
            print(f"Bingo Paper n° {index+1}")
        for card in bingo_paper.cards:
            print(card)
