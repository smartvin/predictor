import numpy as np
import networkx as nx

class MarkovChain:
    def __init__(self):
        self.transition_matrix = {
            ('initial', 'negotiation'): 0.4,
            ('negotiation', 'agreement'): 0.3,
            ('negotiation', 'breakdown'): 0.3,
            ('agreement', 'deal_signed'): 0.8,
            ('breakdown', 'deal_signed'): 0.1,
            ('breakdown', 'negotiation'): 0.4
        }
        self.mc = nx.DiGraph()
        for (state_from, state_to), prob in self.transition_matrix.items():
            self.mc.add_edge(state_from, state_to, weight=prob)

    def determine_next_state(self, current_state):
        if current_state not in self.mc:
            return None
        neighbors = list(self.mc.successors(current_state))
        probabilities = [self.mc[current_state][neighbor]['weight'] for neighbor in neighbors]
        return np.random.choice(neighbors, p=probabilities) if neighbors else None
