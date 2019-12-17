from .utils import human_readable_game_state

class HumanAgent:
    def move(self, state):
        human_readable_game_state(*state)
        move = int(input())
        return move