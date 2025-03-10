import numpy as np
import networkx as nx
from scipy.stats import beta
from transitions import Machine

# Define states and transitions
states = ["initial", "negotiation", "agreement", "breakdown", "deal_signed"]
transitions = [
    {"trigger": "start_negotiation", "source": "initial", "dest": "negotiation"},
    {"trigger": "reach_agreement", "source": "negotiation", "dest": "agreement"},
    {"trigger": "break_down", "source": "negotiation", "dest": "breakdown"},
    {"trigger": "sign_deal", "source": "agreement", "dest": "deal_signed"},
    {"trigger": "retry_negotiation", "source": "breakdown", "dest": "negotiation"}
]

# State Machine class
class NegotiationProcess:
    def __init__(self):
        self.state_machine = Machine(model=self, states=states, transitions=transitions, initial="initial")

# Initialize state machine and Markov Chain
negotiation = NegotiationProcess()

# Initialize transition probabilities (prior beliefs)
transition_matrix = {
    ('initial', 'negotiation'): 0.4,
    ('negotiation', 'agreement'): 0.3,
    ('negotiation', 'breakdown'): 0.3,
    ('agreement', 'deal_signed'): 0.8,
    ('breakdown', 'deal_signed'): 0.1,
    ('breakdown', 'negotiation'): 0.4
}

# Bayesian updating function
def update_transition_probabilities(news_data):
    global transition_matrix
    for (state_from, state_to), prior_prob in transition_matrix.items():
        likelihood = compute_likelihood(news_data, state_from, state_to)
        updated_prob = bayesian_update(prior_prob, likelihood)
        transition_matrix[(state_from, state_to)] = updated_prob
    normalize_transition_matrix()

# Function to compute likelihood from news data
def compute_likelihood(news_data, state_from, state_to):
    relevance_scores = [article['relevance'] for article in news_data if state_from in article['text'] and state_to in article['text']]
    avg_relevance = np.mean(relevance_scores) if relevance_scores else 0.5
    return avg_relevance

# Bayesian update step
def bayesian_update(prior, likelihood, alpha=2, beta_param=2):
    posterior_alpha = alpha + likelihood * 10  # Scale factor for confidence
    posterior_beta = beta_param + (1 - likelihood) * 10
    return beta.mean(posterior_alpha, posterior_beta)

# Normalize transition matrix to ensure probabilities sum to 1
def normalize_transition_matrix():
    global transition_matrix
    for state_from in set([key[0] for key in transition_matrix.keys()]):
        total_prob = sum(transition_matrix[(state_from, state_to)] for state_to in transition_matrix if state_from == state_to[0])
        if total_prob > 0:
            for state_to in transition_matrix:
                if state_from == state_to[0]:
                    transition_matrix[(state_from, state_to)] /= total_prob

# Example function execution
if __name__ == "__main__":
    from fetcher import fetch_news_articles
    
    keywords = ["Ukraine", "Trump", "rare earth deal", "negotiations"]
    news_articles = fetch_news_articles(keywords)
    update_transition_probabilities(news_articles)
    print("Updated Transition Matrix:", transition_matrix)
