import numpy as np
from scipy.stats import beta

class BayesianUpdater:
    def update_transition_probabilities(self, transition_matrix, news_data):
        for (state_from, state_to), prior_prob in transition_matrix.items():
            likelihood = self.compute_likelihood(news_data, state_from, state_to)
            updated_prob = self.bayesian_update(prior_prob, likelihood)
            transition_matrix[(state_from, state_to)] = updated_prob
        self.normalize_transition_matrix(transition_matrix)
        self.update_problog_probabilities(transition_matrix)

    def compute_likelihood(self, news_data, state_from, state_to):
        relevance_scores = [
            article["relevance"]
            for article in news_data
            if state_from in article["text"] and state_to in article["text"]
        ]
        return np.mean(relevance_scores) if relevance_scores else 0.5

    def bayesian_update(self, prior, likelihood, alpha=2, beta_param=2):
        posterior_alpha = alpha + likelihood * 10  # Scale factor for confidence
        posterior_beta = beta_param + (1 - likelihood) * 10
        return beta.mean(posterior_alpha, posterior_beta)

    def normalize_transition_matrix(self, transition_matrix):
        for state_from in set(key[0] for key in transition_matrix.keys()):
            total_prob = sum(
                transition_matrix[(state_from, state_to)]
                for state_to in transition_matrix
                if state_from == state_to[0]
            )
            if total_prob > 0:
                for state_to in transition_matrix:
                    if state_from == state_to[0]:
                        transition_matrix[(state_from, state_to)] /= total_prob

    def update_problog_probabilities(self, transition_matrix, problog_file="problog_model.pl"):
        with open(problog_file, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if line.startswith("probability("):
                key = line.strip().split("(")[1].split(",")[0]
                new_prob = transition_matrix.get((key, "deal_signed"), None)
                if new_prob is not None:
                    new_line = f"probability({key}, {new_prob:.3f}).\n"
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        with open(problog_file, "w") as f:
            f.writelines(new_lines)
