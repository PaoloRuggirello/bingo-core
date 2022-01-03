from bingo import Utils
from bingo.base_model.BaseBingoPaper import BaseBingoPaper
from bingo.base_model.BaseUser import BaseUser


def get_users_with_cards_and_remove_unused_cards(bingo_papers_for_users, n_cards_per_user) -> list:
    users = []
    paper_index = card_index = 0
    for index_user, n_cards in enumerate(n_cards_per_user):
        cards_user = []
        for _ in range(n_cards):
            if card_index > 5:
                card_index = 0
                paper_index += 1
            cards_user.append(bingo_papers_for_users[paper_index].cards[card_index])
            card_index += 1
        users.append(BaseUser(f'Player{index_user + 1}', cards=cards_user))
    bingo_papers_for_users[paper_index].cards = bingo_papers_for_users[paper_index].cards[:card_index]
    return users


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
        elif GAMERS < 1:
            print(f"Number of gamers ({GAMERS}) is less than 1!")
            exit()
    except ValueError as e:
        print(e)
        exit()

    number_of_papers_for_gamers = Utils.get_number_of_papers_needed(sum(N_CARDS))
    bingo_papers = [BaseBingoPaper(is_bank=True, id_paper=0)]

    for i in range(number_of_papers_for_gamers):
        bingo_papers.append(BaseBingoPaper(id_paper=i+1))

    USERS = get_users_with_cards_and_remove_unused_cards(bingo_papers[1:], N_CARDS)
    print("End")
