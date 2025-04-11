import logging
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
import json
import os
from datetime import datetime

class LanguageTranslator:
    def __init__(self, translations_dir="data/translations"):
        self.logger = logging.getLogger(__name__)
        self.supported_languages = {
            'hi': 'Hindi',
            # Add more languages later if needed
        }
        self.translations_dir = translations_dir
        
        # Create translations directory if it doesn't exist
        os.makedirs(self.translations_dir, exist_ok=True)
        
    def detect_language(self, text):
        """
        Detect the language of the input text.
        
        Args:
            text (str): The text to detect language from
            
        Returns:
            str: Language code (e.g., 'hi' for Hindi, 'en' for English)
        """
        if not text or not isinstance(text, str):
            return 'en'  # Default to English if text is empty or not a string
            
        try:
            lang_code = detect(text)
            self.logger.debug(f"Detected language: {lang_code} for text: {text[:50]}...")
            return lang_code
        except LangDetectException as e:
            self.logger.warning(f"Language detection failed: {str(e)} for text: {text[:50]}...")
            return 'en'  # Default to English on detection failure
    
    def translate_text(self, text, source_lang=None, target_lang='en'):
        """
        Translate text from source language to target language.
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code. If None, will be auto-detected
            target_lang (str): Target language code (default: 'en' for English)
            
        Returns:
            dict: Dictionary containing original text, translated text, and language info
        """
        if not text or not isinstance(text, str) or text.strip() == '':
            return {
                'original_text': text,
                'translated_text': text,
                'original_lang': 'en',
                'translated': False
            }
            
        # Detect language if not provided
        if source_lang is None:
            source_lang = self.detect_language(text)
        
        # Don't translate if source is already the target language
        if source_lang == target_lang:
            return {
                'original_text': text,
                'translated_text': text,
                'original_lang': source_lang,
                'translated': False
            }
            
        # Only translate if the language is in our supported list or not English
        if source_lang != 'en' and (source_lang in self.supported_languages or source_lang == 'hi'):
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                translated_text = translator.translate(text)
                self.logger.debug(f"Translated from {source_lang} to {target_lang}")
                
                return {
                    'original_text': text,
                    'translated_text': translated_text,
                    'original_lang': source_lang,
                    'translated': True
                }
            except Exception as e:
                self.logger.error(f"Translation error: {str(e)}")
                
        # Return original if translation failed or wasn't needed
        return {
            'original_text': text,
            'translated_text': text,
            'original_lang': source_lang,
            'translated': False
        }
        
    def process_text_batch(self, texts):
        """
        Process a batch of texts - detect language and translate if needed.
        
        Args:
            texts (list): List of text strings to process
            
        Returns:
            list: List of dictionaries with original and translated texts
        """
        results = []
        for text in texts:
            result = self.translate_text(text)
            results.append(result)
        return results
        
    def save_translations(self, translations_data, query=None):
        """
        Save translations to a JSON file for future reference.
        
        Args:
            translations_data (list): List of translation data dictionaries
            query (str, optional): The search query that produced these tweets
            
        Returns:
            str: Path to the saved file
        """
        # Filter out only tweets that were actually translated
        translated_items = [item for item in translations_data if item.get('translated', False)]
        
        if not translated_items:
            self.logger.info("No translations to save")
            return None
            
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_part = f"_{query}" if query else ""
        filename = f"translations{query_part}_{timestamp}.json"
        filepath = os.path.join(self.translations_dir, filename)
        
        # Write to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': timestamp,
                    'query': query,
                    'count': len(translated_items),
                    'translations': translated_items
                }, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Saved {len(translated_items)} translations to {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Error saving translations: {str(e)}")
            return None
    
    def get_saved_translations(self, tweet_id=None):
        """
        Retrieve saved translations, optionally filtered by tweet ID.
        
        Args:
            tweet_id (str, optional): Specific tweet ID to look for
            
        Returns:
            list: List of translation records
        """
        all_translations = []
        
        try:
            # List all translation files
            for filename in os.listdir(self.translations_dir):
                if not filename.endswith('.json'):
                    continue
                    
                filepath = os.path.join(self.translations_dir, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    translation_data = json.load(f)
                    
                    # If looking for specific tweet, filter the translations
                    if tweet_id:
                        matching_translations = [
                            t for t in translation_data.get('translations', [])
                            if t.get('id') == tweet_id
                        ]
                        if matching_translations:
                            return matching_translations[0]
                    else:
                        all_translations.extend(translation_data.get('translations', []))
            
            return all_translations if not tweet_id else None
            
        except Exception as e:
            self.logger.error(f"Error retrieving translations: {str(e)}")
            return [] if not tweet_id else None