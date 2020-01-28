from thegame import Pan, TIE_VALUE
from q_learning.q_agent import QLearningAgent
from agents.go_with_flow import FlowAgent, FlowAgentDebtAttack
from agents.random_agent import RandomAgent

from collections import Counter

MILION = 10**6
NR_EPISODES = 1*MILION+1

agent = QLearningAgent()#, name='only_hand_value')
board = Pan()

agent.save()
wins = 0
from tqdm import tqdm

def evaluate_agent(agent, other_agent, episodes=1000):
    resultats = []
    board = Pan()

    for i in range(episodes):
        board.restart()
        result = board.play(players=[other_agent, agent])
        resultats.append(result)
    return Counter(resultats)

other_agent = RandomAgent()
players = [agent, other_agent]

for i in tqdm(range(NR_EPISODES)):
    if i == NR_EPISODES//2:
        other_agent = FlowAgent()
    if i == 3*NR_EPISODES//4:
        other_agent = FlowAgentDebtAttack()

    state = board.restart()
    if state[0] == 1:
        move = other_agent.move(state)
        state = board.step(move)
    a_state = state
    move = agent.move(a_state)

    reward = 0
    state = board.state()
    while type(state) is tuple:
        op_move = other_agent.move(state)
        b_state = state = board.step(op_move)
        if type(state) is not tuple:
            break
        move = agent.learn_and_move(a_state, move, reward, b_state)
        a_state = state = board.step(move)
        temp = b_state

    if state == 0:
        reward = 1
    elif state == 1:
        reward = -1
    elif state == 'R':
        reward = TIE_VALUE
    else:
        raise NotImplementedError

    agent.learn(b_state, move, reward, 'T')

    if i%(NR_EPISODES//4)==0 and i > 0:
        #print(agent.states_map.counter)
        print(evaluate_agent(agent, RandomAgent()))
        print(evaluate_agent(agent, FlowAgent()))
        print(evaluate_agent(agent, FlowAgentDebtAttack()))
        agent.save()
        #t_table.save()
print(wins)