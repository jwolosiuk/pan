from .utils import state_to_lol_cards_moves, have_debt, calc_possible_actions_mask

"""
All flow agents willingfully exchange cards, even if they could predict that they will lose.
"""

class FlowAgent:
    """
        Heuristic agent: Put as many card lowest cards as I can. If I can't, take.
    """

    def move(self, state):
        pos = calc_possible_actions_mask(state[1])
        moves = [i for i, v in enumerate(pos) if v is True]
        if len(moves) == 1:
            return moves[0]
        lol = state_to_lol_cards_moves(state)
        move = lol[0][-1]
        return move


class FlowAgentDebtAttack:
    """
        Heuristic agent: Put as many card lowest cards as I can. If I can't, take.
        If I have debt (card which is lower than biggest on stack), put highest card I have
        (try to force opponent to take).
        Note: could put highest card, which forces other player to take/put his highest card.
        Note: could take when it is usefull.
    """

    def move(self, state):
        pos = calc_possible_actions_mask(state[1])
        moves = [i for i, v in enumerate(pos) if v is True]
        if len(moves) == 1:
            return moves[0]
        lol = state_to_lol_cards_moves(state)

        if have_debt(state):
            move = lol[-1][0]
        else:
            move = lol[0][-1]
        return move

class FlowAgentDebtTake:
    """
        Heuristic agent: Put as many card lowest cards as I can. If I can't, take.
        If I have debt (have card which is lower than biggest on stack), take.
    """

    def move(self, state):
        pos = calc_possible_actions_mask(state[1])
        moves = [i for i, v in enumerate(pos) if v is True]
        if len(moves) == 1:
            return moves[0]
        lol = state_to_lol_cards_moves(state)

        if have_debt(state):
            move = 0
        else:
            move = lol[0][-1]
        return move