from thegame import Pan, TIE_VALUE
from agents.utils import state_to_moves
from agents.go_with_flow import FlowAgent

class State:
    def __init__(self, tup_state, me):
        #print(tup_state)
        self.me = me
        self.tup_state = tup_state
        self.terminal = False
        if type(tup_state) == int or tup_state == 'R':
            self.terminal = True
            #print(tup_state)
        else:
            assert tup_state is not None
            self.game = Pan(initial_state=tup_state)
            assert self.game.state() == tup_state

    def getPossibleActions(self):
        moves = state_to_moves(self.tup_state)
        return moves

    def takeAction(self, action):
        next_state = self.game.step(action)
        self.game = Pan(initial_state=self.tup_state)
        #print('takeAction', state_to_moves(self.tup_state), action)
        return State(next_state, me=self.me)

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


FA = FlowAgent()

def flowPolicy(state):
    while not state.isTerminal():
        try:
            action = FA.move(state)
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state.getReward()

class MCTSAgentFlow:
    """
        MCTS agent with time limit
    """
    def __init__(self, time_limit=1000):
        self.mcts = mcts(timeLimit=time_limit, rolloutPolicy=flowPolicy)

    def move(self, state):
        initialState = State(state, me=state[0])
        bestAction = self.mcts.search(initialState=initialState)
        #print('want to take ', bestAction)
        return bestAction