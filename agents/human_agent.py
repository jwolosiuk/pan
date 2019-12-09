from thegame import Pan

def human_readable_game_state(turn, state, possible):
    print("Turn of Player", turn)
    my_hand = state[:6]
    stack = state[6:12]
    rest = state[12:]
    print("Hand:")
    print(sum([[c]*my_hand[i] for i,c in enumerate(Pan.CARDS)], []))
    print("Stack:")
    print(sum([[c] * stack[i] for i, c in enumerate(Pan.CARDS)], ['9K']))
    print("Rest:")
    print(sum([[c] * rest[i] for i, c in enumerate(Pan.CARDS)], []))
    print('Possible actions:')
    if possible[0]:
        print('0 : Take 3 cards')
    for i, is_possible in enumerate(possible[1:]):
        if is_possible:
            card_idx, nr_idx = (i) // 3, (i) % 3
            card = Pan.CARDS[card_idx]
            nr = [1, 3, 4][nr_idx]
            print(i+1,': Put', nr, card,' on top')

class HumanAgent:
    def move(self, state):
        human_readable_game_state(*state)
        move = int(input())
        return move