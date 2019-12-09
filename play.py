from thegame import Pan
from agents.human_agent import HumanAgent

NR_OF_PLAYERS = 2
pan = Pan(nr_of_players=NR_OF_PLAYERS)
state = pan.restart()

players = [HumanAgent(), HumanAgent()]

for i in range(100):
    player_turn = state[0]
    move = players[player_turn].move(state)
    state = pan.step(move)
    if state == 'T':
        print('ok to koniec')
        break

