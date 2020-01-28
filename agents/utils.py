from collections import Counter

from thegame import CARDS, VALUES

def human_readable_game_state(player, state, turns_played):
    print((player,state,turns_played))
    possible = calc_possible_actions_mask(state)
    print("Turn of Player", player, ". Played turns: ", turns_played)
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
    pos = calc_possible_actions_mask(state[1])
    return [i for i,v in enumerate(pos) if v == True]

def state_to_lol_cards_moves(state):
    pos = calc_possible_actions_mask(state[1])
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

def calc_possible_actions_mask(state):
    hand = state[:6]
    stack = state[6:12]
    hand = sum([[c] * hand[i] for i, c in enumerate(CARDS)], [])
    stack = (sum([[c] * stack[i] for i, c in enumerate(CARDS)], []))
    hand_counter = Counter(hand)

    # actions = ['take 3'] + ['play 1 x', 'play 3 x', 'play 4 x'] for x in cards
    possible_actions_mask = []
    possible_actions_mask.append(len(stack) > 0)
    last_on_stack = VALUES[stack[-1]] if len(stack) > 0 else 1
    for card in CARDS:
        l = hand_counter[card]
        possible_actions_mask.append(l >= 1 and VALUES[card] >= last_on_stack)
        possible_actions_mask.append(l >= 3 and VALUES[card] >= last_on_stack)
        possible_actions_mask.append(l >= 4 and VALUES[card] >= last_on_stack)
    return tuple(possible_actions_mask)