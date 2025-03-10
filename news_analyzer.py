import os
from dotenv import load_dotenv
from urllib.parse import quote
import openai
import requests
import json

# API Keys (Replace with your actual keys)
load_dotenv()
NEWS_API_KEY=os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Define the question
topic_question = "Will Trump sign a deal re. rare earth minerals with Ukraine before April 1st?"

# Initialize OpenAI Client
client = openai.Client(api_key=OPENAI_API_KEY)

def generate_search_keywords(question):
    """Use OpenAI to determine relevant search keywords for a topic."""
    prompt = f"Generate a list of relevant search keywords for the topic: {question}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    keywords = response.choices[0].message.content.strip()
    return keywords.split(", ")

def split_keywords(keywords, max_length=500):
    """Split keyword queries to fit within NewsAPI's 500-character limit."""
    queries = []
    current_query = ""
    for keyword in keywords:
        encoded_keyword = quote(keyword)
        if len(current_query) + len(encoded_keyword) + 4 <= max_length:  # +4 for ' OR '
            current_query = f"{current_query} OR {encoded_keyword}" if current_query else encoded_keyword
        else:
            queries.append(current_query)
            current_query = encoded_keyword
    if current_query:
        queries.append(current_query)
    return queries

def fetch_news_articles(keywords):
    """Fetch news articles using NewsAPI while respecting the query length limit."""
    queries = split_keywords(keywords)
    articles = []
    url = "https://newsapi.org/v2/everything"
    for query in queries:
        params = {
            "q": query,
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "sortBy": "relevancy"
        }
        response = requests.get(url, params=params)
        print("received news:", response.json(), "and code=", response.status_code)

        if response.status_code == 200:
            articles.extend(response.json().get("articles", []))
    return articles

def analyze_article(article):
    """Use OpenAI to analyze how an article affects the probability of the event."""
    prompt = (
        f"Determine the effect on likelihood of this article on the question: '{topic_question}'. "
        "Express it with values between -1.0 and 1.0.\n\n"
        "-1.0: Strong No\n"
        "+1.0: Strong Yes\n\n"
        f"Article: {article['title']}\n{article['description']}\n"
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return float(response.choices[0].message.content.strip())

def main():
    # Step 1: Generate keywords
    keywords = generate_search_keywords(topic_question)
    print("Keywords:", keywords)
    
    # Step 2: Fetch news articles
    articles = fetch_news_articles(keywords)
    print(f"Found {len(articles)} articles.")
    
    # Step 3: Analyze articles
    article_scores = {}
    for article in articles[:5]:  # Limit to top 5 articles
        score = analyze_article(article)
        article_scores[article['title']] = score
    
    # Print results
    print(json.dumps(article_scores, indent=2))

if __name__ == "__main__":
    main()