import re
import pandas as pd
from services.language_translator import LanguageTranslator

class DataCleaner:
    def __init__(self):
        self.translator = LanguageTranslator()
    
    def preprocess_tweet(self, tweet: str) -> str:
        """Basic tweet preprocessing without translation"""
        if not isinstance(tweet, str):
            tweet = str(tweet)
        tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
        tweet = re.sub(r'@\w+|#\w+', '', tweet)
        tweet = re.sub(r'\W+', ' ', tweet)
        return tweet.lower()

    def clean_dataframe(self, df: pd.DataFrame, query=None) -> pd.DataFrame:
        """
        Clean dataframe and handle translations in the background
        
        Args:
            df (pd.DataFrame): DataFrame with tweet data
            query (str, optional): Search query that produced these tweets
            
        Returns:
            pd.DataFrame: Cleaned DataFrame with language detection info
        """
        # Drop rows with empty text
        df = df.dropna(subset=['text'])
        df = df[df['text'].str.strip().astype(bool)]
        
        # Apply standard preprocessing
        df['cleaned_text'] = df['text'].apply(self.preprocess_tweet)
        
        # Process translations in the background
        translation_data = []
        
        for _, row in df.iterrows():
            # Detect language
            lang_code = self.translator.detect_language(row['text'])
            
            # Only process non-English text
            if lang_code != 'en':
                translation_result = self.translator.translate_text(row['text'], source_lang=lang_code)
                
                if translation_result['translated']:
                    # Add tweet ID to translation record
                    translation_result['id'] = row['id'] 
                    translation_data.append(translation_result)
                    
                    # Add language info to dataframe
                    df.loc[df['id'] == row['id'], 'original_lang'] = lang_code
            else:
                df.loc[df['id'] == row['id'], 'original_lang'] = 'en'
        
        # Save translations to file if any were found
        if translation_data:
            self.translator.save_translations(translation_data, query)
            
        return df
        
    def get_translation_for_tweet(self, tweet_id):
        """
        Get translation for a specific tweet if available
        
        Args:
            tweet_id (str): Tweet ID to look up
            
        Returns:
            dict: Translation data if found, None otherwise
        """
        return self.translator.get_saved_translations(tweet_id)