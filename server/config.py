from dataclasses import dataclass

@dataclass
class TwitterConfig:
    API_KEY: str = "b22520702amsh1e6776dd467bee7p144615jsn4dde0bcd8ca0"
    API_HOST: str = "twitter154.p.rapidapi.com"
    SEARCH_URL: str = "https://twitter154.p.rapidapi.com/search/search"
    TRENDS_URL: str = "https://twitter154.p.rapidapi.com/trends/"  # Keep the trailing slash
    DEFAULT_SEARCH_PARAMS: dict = None
    DEFAULT_TRENDS_PARAMS: dict = None

    def __post_init__(self):
        self.DEFAULT_SEARCH_PARAMS = {
            "section": "latest",
            "min_retweets": "1",
            "min_likes": "1",
            "limit": "20",
            "language": "en"
        }
        self.DEFAULT_TRENDS_PARAMS = {
            "woeid": "1"
        }