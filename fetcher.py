import requests

class NewsFetcher:
    def __init__(self, api_key):
        self.api_url = "https://api.openai.com/v1/news"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def fetch_articles(self, keywords, count=5):
        params = {"query": " ".join(keywords), "count": count}
        response = requests.get(self.api_url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else []
