import numpy as np
import networkx as nx

class MarkovChain:
    def __init__(self):
        # Define initial transition probabilities
        self.transition_matrix = {
            ('initial', 'negotiation'): 0.4,
            ('negotiation', 'agreement'): 0.3,
            ('negotiation', 'breakdown'): 0.3,
            ('agreement', 'deal_signed'): 0.8,
            ('breakdown', 'deal_signed'): 0.1,
            ('breakdown', 'negotiation'): 0.4
        }

        # Create a directed graph representation
        self.mc = nx.DiGraph()
        for (state_from, state_to), prob in self.transition_matrix.items():
            self.mc.add_edge(state_from, state_to, weight=prob)

