from thegame import Pan, TIE_VALUE
from q_learning.q_agent import QLearningAgent
from agents.go_with_flow import FlowAgent, FlowAgentDebtAttack
from agents.random_agent import RandomAgent

from collections import Counter

MILION = 10**6
NR_EPISODES = 1*MILION+1

agent = QLearningAgent(lr=0.5, gamma=0.95)#, name='only_hand_value')
board = Pan()

agent.save()
wins = 0
from tqdm import tqdm

def evaluate_agent(agent, other_agent, episodes=1000):
    resultats = []
    board = Pan()
    print(agent.Q[2])
    for i in range(episodes):
        board.restart()
        state = board.start_from_state((0, (2, 2, 1, 3, 4, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 1, 0, 4), 0))
        result = board.play(players=[other_agent, agent])
        resultats.append(result)
    return Counter(resultats)

other_agent = FlowAgent()
players = [agent, other_agent]

for i in tqdm(range(NR_EPISODES)):
    if i == NR_EPISODES//2:
        other_agent = FlowAgent()
    #if i == 3*NR_EPISODES//4:
    #    other_agent = FlowAgentDebtAttack()

    state = board.restart()
    state = board.start_from_state((0, (2, 2, 1, 3, 4, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 1, 0, 4), 0))
    if state[0] == 1:
        move = other_agent.move(state)
        state = board.step(move)
    a_state = state
    move = agent.move(a_state)

    reward = 0
    state = board.step(move)
    while type(state) is tuple:
        op_move = other_agent.move(state)
        b_state = state = board.step(op_move)
        if type(state) is not tuple:
            break
        """
        print(a_state)
        print(agent.Q[agent._simplify_state(a_state)])
        print(move)
        print(reward)
        print(b_state)
        print()
        """
        assert a_state[0] == 0
        assert b_state[0] == 0
        move = agent.learn_and_move(a_state, move, reward, b_state)
        a_state = b_state
        state = board.step(move)

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
        print(agent.states_map.counter)
        print(evaluate_agent(agent, RandomAgent()))
        print(evaluate_agent(agent, FlowAgent()))
        print(evaluate_agent(agent, FlowAgentDebtAttack()))
        agent.save()
print(wins)