import requests
import pandas as pd
from typing import Dict, Any, List
from config import TwitterConfig

class TwitterService:
    def __init__(self, config: TwitterConfig):
        self.config = config

    def fetch_tweets(self, query: str) -> pd.DataFrame:
        headers = {
            "x-rapidapi-key": self.config.API_KEY,
            "x-rapidapi-host": self.config.API_HOST
        }
        
        params = {**self.config.DEFAULT_SEARCH_PARAMS, "query": query}
        
        response = requests.get(
            self.config.SEARCH_URL,
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        data = response.json()
        tweets_data = [
            {
                "id": tweet.get("tweet_id"),
                "text": tweet.get("tweet_text", tweet.get("text", "")),
                "timestamp": tweet.get("creation_date"),
                "likes": tweet.get("favorite_count")
            }
            for tweet in data.get("results", [])
        ]
        
        if not tweets_data:
            raise Exception("No tweets found in the response")
        
        return pd.DataFrame(tweets_data)

    def fetch_trends(self, woeid: str = "1") -> List[Dict[str, Any]]:
        headers = {
            "x-rapidapi-key": self.config.API_KEY,
            "x-rapidapi-host": self.config.API_HOST
        }
        
        params = {**self.config.DEFAULT_TRENDS_PARAMS, "woeid": woeid}
        
        response = requests.get(
            self.config.TRENDS_URL,
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"Trends API request failed: {response.status_code} - {response.text}")
        
        data = response.json()
        
        # Extract trends from the response structure
        if not data or not isinstance(data, list) or not data[0].get('trends'):
            raise Exception("Invalid trends data format received")
        
        # Return the trends array directly to maintain original structure
        return data[0]['trends']