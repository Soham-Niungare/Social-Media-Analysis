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
                "favorite_count": int(tweet.get("favorite_count", 0)),
                "retweet_count": int(tweet.get("retweet_count", 0)),
                "reply_count": int(tweet.get("reply_count", 0)),
                "quote_count": int(tweet.get("quote_count", 0)),
                "views": tweet.get("views", 0),
                "user_followers": tweet.get("user", {}).get("follower_count", 0),
                "user_name": tweet.get("user", {}).get("name", ""),
                "user_username": tweet.get("user", {}).get("username", "")
            }
            for tweet in data.get("results", [])
        ]
        
        if not tweets_data:
            raise Exception("No tweets found in the response")
        
        return pd.DataFrame(tweets_data)