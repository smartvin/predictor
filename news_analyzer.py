import os
from dotenv import load_dotenv
import urllib.parse
import openai
import requests
import json
import re

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
    keywords_str = response.choices[0].message.content.strip()
    # Try to extract keywords between quotes (e.g., "keyword")
    keywords_list = re.findall(r'"([^"]+)"', keywords_str)
    if not keywords_list:
        # Fallback: split by newlines and remove numbering (like "1. ")
        keywords_list = [re.sub(r'^\d+\.\s*', '', line).strip() 
                         for line in keywords_str.splitlines() if line.strip()]
    return keywords_list

def split_keywords(keywords, max_length=500):
    """Split keyword queries to fit within NewsAPI's 500-character limit.
       Each keyword is enclosed in quotes for exact matching."""
    queries = []
    current_query = ""
    for keyword in keywords:
        # Enclose the keyword in quotes for exact match:
        keyword_phrase = f'"{keyword}"'
        # If there is already content in current_query, add 4 extra characters for " OR "
        extra = 4 if current_query else 0
        if len(current_query) + len(keyword_phrase) + extra <= max_length:
            current_query = f"{current_query} OR {keyword_phrase}" if current_query else keyword_phrase
        else:
            queries.append(current_query)
            current_query = keyword_phrase
    if current_query:
        print("generated query: ", current_query)
        queries.append(current_query)
    return queries


def fetch_news_articles(keywords):
    """Fetch news articles using NewsAPI while respecting the query length limit."""
    queries = split_keywords(keywords)
    articles = []
    url = "https://newsapi.org/v2/everything"
    for query in queries:
        print("passing query: ", query)
        params = {
            "q": query,
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "sortBy": "relevancy"
        }
        response = requests.get(url, params=params)
        #print("received news:", response.json(), "and code=", response.status_code)

        if response.status_code == 200:
            articles.extend(response.json().get("articles", []))
        else:
            print(f"NewsAPI Error: {response.json()}")
    return articles

def analyze_article(article):
    """Use OpenAI to analyze how an article affects the probability of the event."""
    print("title: ", article["title"], " url: ", article["url"])
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
    
    keywords = ['Trump US Ukraine','Trump US Ukraine rare earth','Ukraine minerals deal']
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