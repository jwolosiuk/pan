import random
from .utils import state_to_moves

class RandomAgent:
    def move(self, state):
        moves = state_to_moves(state)
        return random.choice(moves)