
import requests

API_URL = "https://newsapi.org/v2/everything"

def fetch_news_articles(keywords, api_key="YOUR_API_KEY"):
    print("using API key: ", api_key)
    query = " OR ".join(keywords)
    params = {"q": query, "apiKey": api_key, "language": "en", "sortBy": "relevancy"}
    response = requests.get(API_URL, params=params)
    #print("received response:", response.status_code)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [{"text": article["title"] + " " + article["description"], "relevance": 0.5} for article in articles if article["title"] and article["description"]]
    return []
