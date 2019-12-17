from thegame import Pan
from agents import HumanAgent, RandomAgent, FlowAgent, FlowAgentDebtAttack, FlowAgentDebtTake

NR_OF_PLAYERS = 2
pan = Pan(nr_of_players=NR_OF_PLAYERS)
state = pan.restart()

#players = [RandomAgent(), FlowAgentDebtTake()]

"""
for i in range(100):
    player_turn = state[0]
    move = players[player_turn].move(state)
    state = pan.step(move)
    if state == 'T':
        print('ok to koniec')
        break
"""

#pan.play(players, debug=True)

automatic_agents = [RandomAgent, FlowAgent, FlowAgentDebtTake, FlowAgentDebtAttack]

p1w = [[0 for i in range(4)] for i in range(4)]
p2w = [[0 for i in range(4)] for i in range(4)]

N = 1000

for i1 in range(4):
    for i2 in range(4):
        p1 = automatic_agents[i1]
        p2 = automatic_agents[i2]
        for i in range(N):
            pan.restart()
            win = pan.play(players=[p1(), p2()])
            #c[i1][i2] += 2*win-1
            [p1w, p2w][win][i1][i2] += 1

for i1 in range(4):
    for i2 in range(4):
        if i1<i2:
            continue
        p1 = automatic_agents[i1]
        p2 = automatic_agents[i2]
        print(p1.__name__,'won with', p2.__name__, p1w[i1][i2]/N, 'times when it was P1 and ', p2w[i2][i1]/N,'times when it was P2')

