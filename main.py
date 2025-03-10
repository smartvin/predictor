import os
from dotenv import load_dotenv
from fetcher import fetch_news_articles
from markov_state_machine import NegotiationProcess
from markov_chain import MarkovChain  # Ensure MarkovChain is imported
from bayesian_inference import BayesianInferenceModel


load_dotenv()
NEWS_API_KEY=os.getenv('NEWS_API_KEY')

def main():
    # Initialize components
    state_machine = NegotiationProcess()
    markov_chain = MarkovChain()  # Initialize Markov Chain
    bayesian_model = BayesianInferenceModel()

    # Fetch news articles
    keywords = ["Ukraine", "Trump", "rare earth deal", "negotiations"]
    news_articles = fetch_news_articles(keywords, NEWS_API_KEY)

    # Update Bayesian probabilities from news data
    bayesian_model.update_probabilities_from_news(news_articles)
    
    # Update Markov Chain transition probabilities
    bayesian_model.update_markov_chain(markov_chain.transition_matrix)  # Use MarkovChain's transition matrix
    
    # Determine the next state based on updated probabilities
    current_state = state_machine.state
    print("current state: ", current_state)
    possible_transitions = [
        state_to for (state_from, state_to) in markov_chain.transition_matrix.keys() if state_from == current_state
    ]
    print("found ", len(possible_transitions), " possible transitions")
    for x in possible_transitions:
        print(x)
    if possible_transitions:
        next_state = max(possible_transitions, key=lambda s: markov_chain.transition_matrix.get((current_state, s), 0))
        print("next state is ", next_state)
        state_machine.state_machine.set_state(next_state)

    # Output results
    print("Updated Transition Matrix:", markov_chain.transition_matrix)
    print("Current State:", state_machine.state)

if __name__ == "__main__":
    main()

