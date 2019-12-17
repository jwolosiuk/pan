CARDS = [9, 10, 'J', 'Q', 'K', 'A']

def human_readable_game_state(turn, state, possible):
    print("Turn of Player", turn)
    my_hand = state[:6]
    stack = state[6:12]
    rest = state[12:]
    print("Hand:")
    print(sum([[c]*my_hand[i] for i,c in enumerate(CARDS)], []))
    print("Stack:")
    print(sum([[c] * stack[i] for i, c in enumerate(CARDS)], ['9K']))
    print("Rest:")
    print(sum([[c] * rest[i] for i, c in enumerate(CARDS)], []))
    print('Possible actions:')
    if possible[0]:
        print('0 : Take 3 cards')
    for i, is_possible in enumerate(possible[1:]):
        if is_possible:
            card_idx, nr_idx = (i) // 3, (i) % 3
            card = CARDS[card_idx]
            nr = [1, 3, 4][nr_idx]
            print(i+1,': Put', nr, card,' on top')

def state_to_moves(state):
    pos = state[-1]
    return [i for i,v in enumerate(pos) if v == True]

def state_to_lol_cards_moves(state):
    pos = state[-1]
    lol = [[], [], [], [], [], []]
    for action, v in enumerate(pos[1:], 1):
        card_idx, nr_idx = (action-1) // 3, (action-1) % 3
        if v is True:
            lol[card_idx].append(action)
    lol = [value for value in lol if value != []]
    return lol

def have_debt(state):
    return highest_on_stack(state) > lowest_i_have(state)

def highest_on_stack(state):
    cards = state[1]
    stack = cards[6:12]
    on_stack = sum(stack)
    if on_stack == 0:
        return -1
    m = max([i for i,v in enumerate(stack) if v!=0])
    #print('highest', m)
    return m

def lowest_i_have(state):
    cards = state[1]
    my_hand = cards[0:6]
    m = min([i for i,v in enumerate(my_hand) if v!=0])
    #print('lowest', m)
    return m