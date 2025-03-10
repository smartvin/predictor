import numpy as np
from scipy.stats import beta

class BayesianInferenceModel:
    def __init__(self):
        # Define initial probabilities from the Problog model
        self.probabilities = {
            "financial_gain": 0.8,
            "strategic_alliance": 0.7,
            "foreign_aid": 0.9,
            "nato_support": 0.6,
            "us_military_aid": 0.5,
            "energy_access": 0.6,
            "geopolitical_influence": 0.75,
            "economic_benefits": 0.7,
            "strategic_advantage": 0.8,
            "public_opposition": 0.6,
            "sovereignty_concerns": 0.7,
            "russian_reaction": 0.6,
            "political_risk": 0.5,
            "political_opposition": 0.8,
            "legal_barriers": 0.6,
            "diplomatic_risk": 0.5
        }
        
    def bayesian_update(self, key, likelihood, alpha=2, beta_param=2):
        """Update a probability using Bayesian inference."""
        if key not in self.probabilities:
            raise ValueError(f"Unknown probability key: {key}")
        
        prior = self.probabilities[key]
        posterior_alpha = alpha + likelihood * 10
        posterior_beta = beta_param + (1 - likelihood) * 10
        updated_prob = beta.mean(posterior_alpha, posterior_beta)
        
        self.probabilities[key] = updated_prob

    def update_probabilities_from_news(self, news_data):
        """Iterate over news articles to update probabilities."""
        for key in self.probabilities.keys():
            relevance_scores = [article["relevance"] for article in news_data if key in article["text"]]
            likelihood = np.mean(relevance_scores) if relevance_scores else 0.5
            self.bayesian_update(key, likelihood)
        
    def get_probabilities(self):
        """Return the updated probability dictionary."""
        return self.probabilities

    def update_markov_chain(self, transition_matrix):
        """Update the Markov Chain transition probabilities based on Bayesian updates."""
        for (state_from, state_to) in transition_matrix.keys():
            print("transitioning from:", state_from," to ", state_to)
            if state_to in self.probabilities:
                transition_matrix[(state_from, state_to)] = self.probabilities[state_to]
        
        # Normalize transitions
        for state_from in set(key[0] for key in transition_matrix.keys()):
            print("state_to is:", state_to)
            total_prob = sum(transition_matrix[(state_from, state_to)] for state_to in transition_matrix if state_from == state_to)
            if total_prob > 0:
                for state_to in transition_matrix:
                    if state_from == state_to[0]:
                        transition_matrix[(state_from, state_to)] /= total_prob
