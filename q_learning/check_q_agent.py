from thegame import Pan
from q_learning.q_agent import QLearningAgent

QA = QLearningAgent()
QA.load('q_tables/agent_QLearningAgent_trained:6071842')
print(len(QA.states_map))