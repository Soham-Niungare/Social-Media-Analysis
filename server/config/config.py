from dataclasses import dataclass

@dataclass
class TwitterConfig:
    API_KEY: str = "6c80c82d04mshcc770f8485ad426p1f8822jsn04464e6a0a17"
    API_HOST: str = "twitter154.p.rapidapi.com"
    SEARCH_URL: str = "https://twitter154.p.rapidapi.com/search/search"
    TRENDS_URL: str = "https://twitter154.p.rapidapi.com/trends/"  
    DEFAULT_SEARCH_PARAMS: dict = None
    DEFAULT_TRENDS_PARAMS: dict = None

    def __post_init__(self):
        self.DEFAULT_SEARCH_PARAMS = {
            "section": "top",
            "min_retweets": "1",
            "min_likes": "1",
            "limit": "20"
            # "language": "en"
        }
        self.DEFAULT_TRENDS_PARAMS = {
            "woeid": "1"
        }