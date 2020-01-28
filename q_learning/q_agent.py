import numpy as np
import pickle
from collections import defaultdict
from agents.utils import state_to_moves, calc_possible_actions_mask
from numpy.ma import masked_array

class HashIncrementer(defaultdict):
    def __init__(self, start_from=1):
        self.counter = start_from

    def __missing__(self, key):
        self[key] = self.counter
        self.counter += 1
        return self.counter-1

class QLearningAgent():
    NR_OF_MOVES = 19

    def __init__(self, lr=0.1, gamma=0.95, name='agent'):
        self.lr = lr
        self.gamma = gamma
        self.Q = np.zeros((10000000, self.NR_OF_MOVES)) + 0.001 # len(obs),len(acts)
        self.Q[0] = 0
        self.Q[1] = 0
        self.situations_learned = 0
        self.states_map = HashIncrementer(start_from=2)
        self.name = name

    def save(self):
        filename = f'q_tables/{self.name}_{self.__class__.__name__}_trained:{self.situations_learned}'
        np.save(filename, self.Q)
        pickle.dump(self.states_map, open(filename + "_states_map.p", "wb"))

    def load(self, filename):
        self.Q = np.load(filename+'.npy', allow_pickle=True)
        self.states_map = pickle.load(open(filename + "_states_map.p", "rb"))

    def learn_and_move(self, last_state, last_action, got_reward, new_state):  # with exploration
        self.learn(last_state, last_action, got_reward, new_state)

        exploration = np.random.rand() < 0.01
        if not exploration:
            next_action = self.move(new_state)
        else:
            moves = state_to_moves(new_state)
            next_action = moves[np.random.randint(0, len(moves))]
        return next_action

    def learn(self, state, action, reward, new_state):
        s = self._simplify_state(state)
        a = action
        r = reward
        s1 = self._simplify_state(new_state)
        if type(new_state) is not tuple:
            masked = [0]
        else:
            pos_mask = calc_possible_actions_mask(new_state[1])
            masked = masked_array(self.Q[s1], mask=~np.array(pos_mask))
        self.Q[s, a] = self.Q[s, a] + self.lr * (r + self.gamma * np.max(masked) - self.Q[s, a])
        self.situations_learned += 1

    def move(self, state):  # greedy
        s = self._simplify_state(state)
        #print(s)
        pos_mask = calc_possible_actions_mask(state[1])
        #print(self.Q[s])
        #print(pos_mask)
        masked = masked_array(self.Q[s], mask=~np.array(pos_mask))
        #print(masked)
        a = masked.argmax()
        return a

    def _simplify_state(self, state):  # state to number [0-n]
        if state == 'R':
            return 1
        if type(state) != tuple:
            return 0
        return self.states_map[state[:2]]