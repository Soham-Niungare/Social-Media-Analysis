import re
import pandas as pd

class DataCleaner:
    @staticmethod
    def preprocess_tweet(tweet: str) -> str:
        if not isinstance(tweet, str):
            tweet = str(tweet)
        tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
        tweet = re.sub(r'@\w+|#\w+', '', tweet)
        tweet = re.sub(r'\W+', ' ', tweet)
        return tweet.lower()

    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(subset=['text'])
        df = df[df['text'].str.strip().astype(bool)]
        df['cleaned_text'] = df['text'].apply(DataCleaner.preprocess_tweet)
        return df