import re
import pandas as pd
from services.language_translator import LanguageTranslator

class DataCleaner:
    def __init__(self):
        self.translator = LanguageTranslator()
    
    def preprocess_tweet(self, tweet: str) -> str:
        if not isinstance(tweet, str):
            tweet = str(tweet)
        tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
        tweet = re.sub(r'@\w+|#\w+', '', tweet)
        tweet = re.sub(r'\W+', ' ', tweet)
        return tweet.lower()

    def clean_dataframe(self, df: pd.DataFrame, query=None) -> pd.DataFrame:
        df = df.dropna(subset=['text'])
        df = df[df['text'].str.strip().astype(bool)]
        
        df['cleaned_text'] = df['text'].apply(self.preprocess_tweet)
        
        translation_data = []
        
        for _, row in df.iterrows():
            lang_code = self.translator.detect_language(row['text'])
            
            if lang_code != 'en':
                translation_result = self.translator.translate_text(row['text'], source_lang=lang_code)
                
                if translation_result['translated']:
                    translation_result['id'] = row['id'] 
                    translation_data.append(translation_result)
                    
                    df.loc[df['id'] == row['id'], 'original_lang'] = lang_code
            else:
                df.loc[df['id'] == row['id'], 'original_lang'] = 'en'
        
        if translation_data:
            self.translator.save_translations(translation_data, query)
            
        return df
        
    def get_translation_for_tweet(self, tweet_id):
        return self.translator.get_saved_translations(tweet_id)