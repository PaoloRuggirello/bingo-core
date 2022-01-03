from bingo import Utils
from bingo.base_model.BaseBingoPaper import BaseBingoPaper
from bingo.base_model.BaseUser import BaseUser
from bingo.Prize import Prize


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
    # remove unused cards
    bingo_papers_for_users[paper_index].cards = bingo_papers_for_users[paper_index].cards[:card_index]
    return users


def get_user_and_card_by_id_card(id_card, users) -> tuple:
    for user in users:
        for card in user.user_cards:
            if card.id_card == id_card:
                return user, card
    return None, None


if __name__ == '__main__':
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

    print('Game is ready to start.\n\nBank is set and these are the players:')
    for user in USERS:
        print(f'{user.nickname} with cards: ')
        for card in user.user_cards:
            print(card)

    # initialization of values for game
    prizes = Prize.list()
    prize_index = 0
    NUMBERS_NOT_EXTRACTED = Utils.PAPER_NUMBERS
    exit_condition = False

    while not exit_condition:
        input('Press ENTER to extract new number')
        new_number, NUMBERS_NOT_EXTRACTED = Utils.np_pop_random(NUMBERS_NOT_EXTRACTED)
        card_and_winners = {}
        for paper in bingo_papers:
            card_and_winners.update(paper.get_cards_with_number_and_winner(new_number, prizes[prize_index]))
        print(f'Extracted number is {new_number}')
        print('The number is present in those cards: ', end='')
        for id_card in card_and_winners:
            print(f'{id_card}, ', end='')
        print()
        # getting possible winners
        winners = {k: v for k, v in card_and_winners.items() if v}
        if len(winners) > 0:
            print(f'{Prize(prizes[prize_index]).name} winners:')
            for card_id in winners:
                if card_id <= 6:
                    print('Bank')
                    print(bingo_papers[0].cards[card_id - 1])
                else:
                    user_winner, card_winner = get_user_and_card_by_id_card(card_id, USERS)
                    print(user_winner.nickname)
                    print(card_winner)
            prize_index += 1

        exit_condition = len(NUMBERS_NOT_EXTRACTED) == 0 or prize_index >= len(prizes)

