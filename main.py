from fetcher import NewsFetcher
from markov_chain import MarkovChain
from markov_state_machine import NegotiationProcess, update_transition_probabilities  # Ensure this matches your filename


API_KEY = "<API KEY>"  # Replace with your API key

def main():
    # Initialize components
    fetcher = NewsFetcher(API_KEY)
    markov = MarkovChain()
    state_machine = NegotiationProcess()

    # Fetch news articles
    keywords = ["Ukraine", "Trump", "rare earth deal", "negotiations"]
    news_articles = fetcher.fetch_articles(keywords)

    # Update transition probabilities
    update_transition_probabilities(news_articles, markov.transition_matrix)

    # Determine the next state and trigger the transition
    next_state = markov.determine_next_state(state_machine.state_machine.state)
    if next_state:
        state_machine.state_machine.set_state(next_state)

    # Output updated probabilities
    print("Updated Transition Matrix:", markov.transition_matrix)

if __name__ == "__main__":
    main()