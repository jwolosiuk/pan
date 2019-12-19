from thegame import Pan
from agents import HumanAgent, RandomAgent, FlowAgent, FlowAgentDebtAttack, FlowAgentDebtTake
from mcts_agents import SimpleMCTSAgent

NR_OF_PLAYERS = 2
pan = Pan(nr_of_players=NR_OF_PLAYERS)
state = pan.restart()

players = [SimpleMCTSAgent(), HumanAgent()]
pan.play(players, debug=True)

"""
state = pan.start_from_state((0, (3,4,4,0,4,3,0,0,0,4,0,0,0,0,0,0,0,1)))
print(state)
print(pan.play(players, debug=True))
"""


"""
for i in range(100):
    player_turn = state[0]
    move = players[player_turn].move(state)
    state = pan.step(move)
    if state == 'T':
        print('ok to koniec')
        break
"""
"""

automatic_agents = [RandomAgent, FlowAgent, FlowAgentDebtTake, FlowAgentDebtAttack, SimpleMCTSAgent]

nr = len(automatic_agents)
p1w = [[0 for i in range(nr)] for i in range(nr)]
p2w = [[0 for i in range(nr)] for i in range(nr)]
ties = [[0 for i in range(nr)] for i in range(nr)]

N = 100

#for i1 in range(nr):
for i1 in range(nr):
    for i2 in range(nr-1):
        p1 = automatic_agents[i1]
        p2 = automatic_agents[i2]
        for i in range(N):
            pan.restart()
            win = pan.play(players=[p1(), p2()])
            #c[i1][i2] += 2*win-1
            {0:p1w, 1:p2w, 'R':ties}[win][i1][i2] += 1

for i1 in range(nr):
    for i2 in range(nr):
        if i1<i2:
            continue
        p1 = automatic_agents[i1]
        p2 = automatic_agents[i2]
        print(p1.__name__,'won with', p2.__name__, p1w[i1][i2]/N, 'times when it was P1 and ', p2w[i2][i1]/N,'times when it was P2 and tied', ties[i1][i2], ties[i2][i1],'times')
"""
"""
Some statistics, if being p1 or p2 makes difference? It shouldnt, as starting player and everything else is randomized.
"""