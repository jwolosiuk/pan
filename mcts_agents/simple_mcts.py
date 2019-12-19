import numpy as np

import thegame
import agents

class SimpleMCTSAgent:
    """
        MCTS agent with depth one
    """
    def __init__(self, nr_of_sims=1, me=agents.FlowAgentDebtAttack, opponent=agents.FlowAgentDebtAttack):
        self.NR_OF_SIMS = nr_of_sims
        self.me_agent = me()
        self.opponent_agent = opponent()

    def move(self, state):
        me_turn = state[0]
        pos = state[-1]
        moves = [i for i, v in enumerate(pos) if v is True]
        wins = [0 for i in range(len(moves))]
        nr_of_moves = [np.inf for i in range(len(moves))]

        agents = [self.me_agent, self.opponent_agent]
        if me_turn != 0:
            agents.reverse()

        for i, m in enumerate(moves):
            for _ in range(self.NR_OF_SIMS):
                sim = thegame.Pan(initial_state=state)
                n = sim.step(m)
                #print(n)
                win = sim.play(players=agents)
                if win == me_turn:
                    wins[i] += 1
                    if nr_of_moves[i] == np.inf:
                        nr_of_moves[i] = 0
                    nr_of_moves[i] += sim.turns_played

        maxi = max(wins)
        best_moves = [i for i, v in enumerate(wins) if v == maxi]
        mini = min(nr_of_moves)
        fastest_wins = [i for i, v in enumerate(nr_of_moves) if v == mini]
        #print(wins)
        #print(nr_of_moves)
        #print(fastest_wins)
        return moves[fastest_wins[0]]