import requests
import pandas as pd
from typing import Dict, Any, List
from config.config import TwitterConfig
import logging
import time

class TwitterService:
    def __init__(self, config: TwitterConfig):
        self.config = config
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def fetch_tweets(self, query: str) -> pd.DataFrame:
        headers = {
            "x-rapidapi-key": self.config.API_KEY,
            "x-rapidapi-host": self.config.API_HOST
        }
        
        all_tweets_data = []
        params = {**self.config.DEFAULT_SEARCH_PARAMS, "query": query}
        

        self.logger.debug(f"Initial search parameters: {params}")
        

        try:
            response = requests.get(
                self.config.SEARCH_URL,
                headers=headers,
                params=params
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed: {response.status_code} - {response.text}")
            
            data = response.json()

            self.logger.debug(f"Initial response keys: {data.keys()}")
            self.logger.debug(f"Number of initial results: {len(data.get('results', []))}")
            
            initial_tweets = data.get("results", [])
            all_tweets_data.extend([self._process_tweet_data(tweet) for tweet in initial_tweets])
            

            continuation_token = data.get("continuation_token")
            self.logger.debug(f"Continuation token received: {continuation_token is not None}")
            
            page = 1
            max_pages = 8  # Limit pages for testin
            
            while continuation_token and page < max_pages:
                self.logger.debug(f"Fetching page {page + 1}")
                time.sleep(1)  # Rate limitin
                
                continuation_params = {
                    **params,
                    "continuation_token": continuation_token
                }
                

                self.logger.debug(f"Continuation parameters: {continuation_params}")
                
                try:
                    continuation_url = f"{self.config.SEARCH_URL}/continuation"
                    self.logger.debug(f"Continuation URL: {continuation_url}")
                    
                    response = requests.get(
                        continuation_url,
                        headers=headers,
                        params=continuation_params
                    )
                    
                    if response.status_code != 200:
                        self.logger.error(f"Continuation request failed: {response.status_code}")
                        break
                    
                    cont_data = response.json()

                    self.logger.debug(f"Continuation response keys: {cont_data.keys()}")
                    self.logger.debug(f"Number of continuation results: {len(cont_data.get('results', []))}")
                    
                    new_tweets = cont_data.get("results", [])
                    if not new_tweets:
                        self.logger.debug("No new tweets in continuation response")
                        break
                    
                    all_tweets_data.extend([self._process_tweet_data(tweet) for tweet in new_tweets])
                    self.logger.debug(f"Total tweets collected so far: {len(all_tweets_data)}")
                    
                    continuation_token = cont_data.get("continuation_token")
                    self.logger.debug(f"New continuation token received: {continuation_token is not None}")
                    
                    page += 1
                    
                except Exception as e:
                    self.logger.error(f"Error in continuation request: {str(e)}")
                    break
                    
        except Exception as e:
            self.logger.error(f"Error in initial request: {str(e)}")
            raise e
        
        if not all_tweets_data:
            raise Exception("No tweets found in the response")
        
        df = pd.DataFrame(all_tweets_data)
        self.logger.debug(f"Final DataFrame shape: {df.shape}")
        return df

    def _process_tweet_data(self, tweet: Dict) -> Dict:
        """Helper method to process tweet data remains unchanged"""
        return {
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

    def fetch_trends(self, woeid: str = "1") -> List[Dict[str, Any]]:

        self.logger.debug(f"Fetching trends for WOEID: {woeid}")
        
        headers = {
            "x-rapidapi-key": self.config.API_KEY,
            "x-rapidapi-host": self.config.API_HOST
        }
        
        querystring = {"woeid": woeid}
        
        try:
            self.logger.debug(f"Making request to: {self.config.TRENDS_URL}")
            response = requests.get(
                self.config.TRENDS_URL,
                headers=headers,
                params=querystring
            )
            
            self.logger.debug(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                error_msg = f"API request failed: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                raise Exception(error_msg)
            
            response_data = response.json()
            self.logger.debug(f"Raw API response: {response_data}")
            

            if not response_data or not isinstance(response_data, list) or len(response_data) == 0:
                self.logger.warning("Invalid response format")
                return []
                
            trends = response_data[0].get("trends", [])
            if not trends:
                self.logger.warning("No trends found in the response")
                return []
            
            formatted_trends = []
            for index, trend in enumerate(trends):
                if not trend.get("name"):
                    continue
                    
                formatted_trend = {
                    "name": trend.get("name", ""),
                    "url": trend.get("url", ""),
                    "tweet_volume": trend.get("tweet_volume", 0) or 0,
                    "rank": index + 1,
                    "query": trend.get("query", ""),
                    "promoted_content": trend.get("promoted_content", None)
                }
                formatted_trends.append(formatted_trend)
            
            self.logger.debug(f"Formatted {len(formatted_trends)} trends")
            return formatted_trends
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error while fetching trends: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error while fetching trends: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)