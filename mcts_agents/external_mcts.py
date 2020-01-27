from thegame import Pan, MAX_TURNS
from agents.utils import state_to_moves

TIE_VALUE = -0.9

class State:
    def __init__(self, tup_state, me, turns_played=0):
        #print(tup_state)
        self.me = me
        self.tup_state = tup_state
        self.turns_played = turns_played
        self.terminal = False
        if type(tup_state) == int or tup_state == 'R':
            self.terminal = True
            #print(tup_state)
        else:
            assert tup_state is not None
            self.game = Pan(initial_state=tup_state)
            self.game.turns_played = turns_played
            assert self.game.state() == tup_state

    def getPossibleActions(self):
        moves = state_to_moves(self.tup_state)
        return moves

    def takeAction(self, action):
        next_state = self.game.step(action)
        turns_played = self.game.turns_played
        self.game = Pan(initial_state=self.tup_state)
        #print('takeAction', state_to_moves(self.tup_state), action)
        return State(next_state, me=self.me, turns_played=turns_played)

    def isTerminal(self):
        #hands = self.tup_state[1]
        #if sum(hands[:6]) == 0 or sum(hands[-6:]) == 0:
        #    return True
        #return False
        return self.terminal

    def getReward(self):
        """hands = self.tup_state[1]
        if sum(hands[:6]) == 0:
            return 1
        if sum(hands[-6:]) == 0:
            return -1
        else:
            return 0
        """
        if not self.isTerminal():
            return 0
        else:
            if self.tup_state == self.me:
                return 1
            elif self.tup_state == 'R':
                return TIE_VALUE
            else:
                return -1

from mcts import mcts

class MCTSAgent:
    """
        MCTS agent with time limit
    """
    def __init__(self, time_limit=1000):
        self.mcts = mcts(timeLimit=time_limit)

    def move(self, state):
        initialState = State(state, me=state[0])
        bestAction = self.mcts.search(initialState=initialState)
        #print('want to take ', bestAction)
        return bestAction