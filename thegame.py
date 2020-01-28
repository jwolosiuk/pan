import random
import math
from collections import Counter

MAX_TURNS = 50
TIE_VALUE = -0.9
CARDS = [9, 10, 'J', 'Q', 'K', 'A']
STARTING_CARD = '9K'
VALUES = {v: i + 1 for i, v in enumerate(CARDS)}

from agents.utils import human_readable_game_state, calc_possible_actions_mask

class Pan:


    def __init__(self, initial_state=None, nr_of_players=2):
        self.NR_OF_PLAYERS = nr_of_players
        self.HAND_SIZE = math.ceil(len(CARDS)*4/self.NR_OF_PLAYERS)

        if initial_state is None:
            self.restart()
        else:
            self.start_from_state(initial_state)

    def play(self, players=None, debug=False):
        if players is None:
            raise Exception("Pass players")
        state = self.state()
        while type(state) is tuple:
            if debug:
                human_readable_game_state(*state)
            turn = state[0]
            player = players[turn]
            move = player.move(state)
            if debug:
                print("Player",turn,'-', player.__class__.__name__ ,"moves",move)
            state = self.step(move)
        if debug:
            print("Won player ", state, '-', player.__class__.__name__ )
            print("Nr of turns", self.turns_played)
        return state

    def start_from_state(self, initial_state):
        self.clean_game()

        turn, hands = initial_state[0:2]
        self._turn = turn

        stack = sum([[CARDS[i]]*v for i,v in enumerate(hands[6:12])], [])
        self.stack = stack

        hands = [hands[:6], hands[-6:]]
        hands = [Counter({k: v for k, v in zip(CARDS, h)}) for h in hands]
        if turn != 0:
            hands.reverse()
        self.hands = hands
        #print('startState', self.hands)
        #print('startState', self.state())
        self.turns_played = initial_state[-1]
        return self.state()

    def restart(self):
        self.clean_game()

        self._deck = CARDS.copy() * 4
        self._deck[0] = STARTING_CARD  # 9 kier, zeby wylosowac pierwszego gracza i wgle
        random.shuffle(self._deck)
        self.hands = [self._deck[i:i+self.HAND_SIZE] for i in range(0, len(self._deck), self.HAND_SIZE)]
        random.shuffle(self.hands)

        self.first_player = None
        for pi, hand in enumerate(self.hands):
            if STARTING_CARD in hand:
                self.first_player = pi
                hand.remove(STARTING_CARD)
                break

        self.hands = [Counter(hand) for hand in self.hands]
        self._turn = self.rotate_next(self.first_player)
        return self.state()

    def clean_game(self):
        self.stack = []
        self.turns_played = 0
        self.remaining_players = self.NR_OF_PLAYERS

    @property
    def turn(self):
        return self._turn

    def step(self, action):
        # actions = ['take 3'] + ['play 1 x', 'play 3 x', 'play 4 x'] for x in cards

        hand = self.hands[self.turn]
        possible_actions_mask = calc_possible_actions_mask(self.state()[1])
        if possible_actions_mask[action] is False:
            print('cant do', self.state())
            print('cant do', hand)
            print('cant do', self.turn)
            print('cant do', possible_actions_mask)
            print('cant do action', action)
            raise EnvironmentError('Cant do the action')
        else:
            # DO THE ACTION
            if action == 0:
                picked_cards = self.stack[-3:]
                del self.stack[-3:]
                hand += Counter(picked_cards)
            else:
                card_idx, nr_idx = (action-1)//3, (action-1)%3
                card = CARDS[card_idx]
                nr = [1, 3, 4][nr_idx]

                hand[card] -= nr
                self.stack.extend([card]*nr)

        endgame = self.end_turn()
        if endgame is not None:
            # koniec gry
            return endgame

        return self.state()

    def state(self):
        hand = self.hands[self.turn]
        next_turn = self.rotate_next(self.turn)
        next_hand = self.hands[next_turn]

        if sum(hand.values()) == 0:
            return self.turn
        if sum(next_hand.values()) == 0:
            return next_turn
        if self.turns_played > MAX_TURNS:
            return 'R'

        #possible_actions_mask = self.calc_possible_actions_mask(hand)

        # game_state = p1 hand counters + stack counters [+ p2 stack counters]
        rest = self._hand_to_tuple(next_hand)
        #seen = self._hand_to_tuple(Counter(self.stack)+hand)
        #rest = tuple(4 - s + (-1 if i == 0 else 0) for i, s in enumerate(seen))
        state = self._hand_to_tuple(hand) + \
                self._hand_to_tuple(self.stack) + \
                rest
        # print(state)
        # print(sum(state))
        assert sum(state) == 23
        return self.turn, state, self.turns_played

    def _hand_to_tuple(self, hand):
        sorted_hand = []
        ph = Counter(hand)

        for card in CARDS:
            l = ph[card]
            sorted_hand.append(l)
        return tuple(sorted_hand)

    def rotate_next(self, start):
        i = start
        return (i+1) % self.NR_OF_PLAYERS

    def end_turn(self):
        # assert all([self.values[a] >= self.values[b] for a,b in zip(self.stack[1:], self.stack)])
        self.turns_played += 1
        last_turn = self._turn
        next_turn = self.rotate_next(self._turn)
        hand = self.hands[self._turn]
        if sum(hand.values()) == 0:
            #print('Player '+str(self._turn)+ ' ended game')
            self.remaining_players -= 1
            return self._turn

        if self.remaining_players <= 1:
            raise RuntimeError  # shouldnt be here

        while sum(self.hands[next_turn].values()) == 0:
            next_turn = self.rotate_next(next_turn)
        if next_turn == last_turn:
            print('wow, the seccond if ends the game')
            raise RuntimeError  # shouldnt be here
        self._turn = next_turn

    def close(self):
        pass