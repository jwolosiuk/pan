import random
import math
from collections import Counter

class Pan:
    CARDS = [9, 10, 'J', 'Q', 'K', 'A']
    STARTING_CARD = '9K'
    values = {v: i + 1 for i, v in enumerate(CARDS)}

    def __init__(self, nr_of_players=2):
        self.NR_OF_PLAYERS = nr_of_players
        self.restart()

    def restart(self):
        self._deck = self.CARDS.copy()*4
        self.HAND_SIZE = math.ceil(len(self._deck)/self.NR_OF_PLAYERS)
        self._deck[0] = self.STARTING_CARD  # 9 kier, zeby wylosowac pierwszego gracza i wgle
        random.shuffle(self._deck)
        self.hands = [self._deck[i:i+self.HAND_SIZE] for i in range(0, len(self._deck), self.HAND_SIZE)]
        random.shuffle(self.hands)

        self.first_player = None
        for pi, hand in enumerate(self.hands):
            if self.STARTING_CARD in hand:
                self.first_player = pi
                hand.remove(self.STARTING_CARD)
                break

        self.hands = [Counter(hand) for hand in self.hands]

        self.stack = []
        self._turn = self.rotate_next(self.first_player)
        self.turns_played = 0
        self.remaining_players = self.NR_OF_PLAYERS
        return self.state()

    @property
    def turn(self):
        return self._turn

    def step(self, action):
        # actions = ['take 3'] + ['play 1 x', 'play 3 x', 'play 4 x'] for x in cards

        hand = self.hands[self.turn]
        possible_actions_mask = self.calc_possible_actions_mask(hand)
        if possible_actions_mask[action] is False:
            raise EnvironmentError('Cant do the action')
        else:
            # DO THE ACTION
            if action == 0:
                picked_cards = self.stack[-3:]
                del self.stack[-3:]
                hand += Counter(picked_cards)
            else:
                card_idx, nr_idx = (action-1)//3, (action-1)%3
                card = self.CARDS[card_idx]
                nr = [1, 3, 4][nr_idx]

                hand[card] -= nr
                self.stack.extend([card]*nr)

        endgame = self.end_turn()
        if endgame is not None:
            # koniec gry
            return 'T'

        return self.state()

    def state(self):
        hand = self.hands[self.turn]
        next_turn = self.rotate_next(self.turn)
        possible_actions_mask = self.calc_possible_actions_mask(hand)

        # game_state = p1 hand counters + stack counters [+ p2 stack counters]
        seen = self._hand_to_tuple(Counter(self.stack)+hand)
        rest = tuple(4 - s + (-1 if i == 0 else 0) for i, s in enumerate(seen))
        state = self._hand_to_tuple(hand) + \
                self._hand_to_tuple(self.stack) + \
                rest
        return self.turn, state, possible_actions_mask

    def calc_possible_actions_mask(self, hand):
        hand_counter = Counter(hand)

        # actions = ['take 3'] + ['play 1 x', 'play 3 x', 'play 4 x'] for x in cards
        possible_actions_mask = []
        possible_actions_mask.append(len(self.stack) > 0)
        last_on_stack = self.values[self.stack[-1]] if len(self.stack) > 0 else 1
        for card in self.CARDS:
            l = hand_counter[card]
            possible_actions_mask.append(l >= 1 and self.values[card] >= last_on_stack)
            possible_actions_mask.append(l >= 3 and self.values[card] >= last_on_stack)
            possible_actions_mask.append(l >= 4 and self.values[card] >= last_on_stack)
        return tuple(possible_actions_mask)

    def _hand_to_tuple(self, hand):
        sorted_hand = []
        ph = Counter(hand)

        for card in self.CARDS:
            l = ph[card]
            sorted_hand.append(l)
        return tuple(sorted_hand)

    def rotate_next(self, start):
        i = start
        return (i+1) % self.NR_OF_PLAYERS

    def end_turn(self):
        assert all([self.values[a] >= self.values[b] for a,b in zip(self.stack[1:], self.stack)])
        self.turns_played += 1
        last_turn = self._turn
        next_turn = self.rotate_next(self._turn)
        hand = self.hands[self._turn]
        if sum(hand.values()) == 0:
            print('Player '+str(self._turn)+ ' ended game')
            self.remaining_players -= 1

        if self.remaining_players <= 1:
            return 'T'

        while sum(self.hands[next_turn].values()) == 0:
            next_turn = self.rotate_next(next_turn)
        if next_turn == last_turn:
            print('wow, the seccond if ends the game')
            return 'T'
        self._turn = next_turn

    def close(self):
        pass