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
        }
        self.translations_dir = translations_dir
        
        os.makedirs(self.translations_dir, exist_ok=True)
        
    def detect_language(self, text):
        if not text or not isinstance(text, str):
            return 'en'  
            
        try:
            lang_code = detect(text)
            self.logger.debug(f"Detected language: {lang_code} for text: {text[:50]}...")
            return lang_code
        except LangDetectException as e:
            self.logger.warning(f"Language detection failed: {str(e)} for text: {text[:50]}...")
            return 'en'  
    
    def translate_text(self, text, source_lang=None, target_lang='en'):
        if not text or not isinstance(text, str) or text.strip() == '':
            return {
                'original_text': text,
                'translated_text': text,
                'original_lang': 'en',
                'translated': False
            }
            
        if source_lang is None:
            source_lang = self.detect_language(text)
        

        if source_lang == target_lang:
            return {
                'original_text': text,
                'translated_text': text,
                'original_lang': source_lang,
                'translated': False
            }
            

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
                

        return {
            'original_text': text,
            'translated_text': text,
            'original_lang': source_lang,
            'translated': False
        }
        
    def process_text_batch(self, texts):

        results = []
        for text in texts:
            result = self.translate_text(text)
            results.append(result)
        return results
        
    def save_translations(self, translations_data, query=None):


        translated_items = [item for item in translations_data if item.get('translated', False)]
        
        if not translated_items:
            self.logger.info("No translations to save")
            return None
            

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_part = f"_{query}" if query else ""
        filename = f"translations{query_part}_{timestamp}.json"
        filepath = os.path.join(self.translations_dir, filename)
        

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

        all_translations = []
        
        try:

            for filename in os.listdir(self.translations_dir):
                if not filename.endswith('.json'):
                    continue
                    
                filepath = os.path.join(self.translations_dir, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    translation_data = json.load(f)
                    

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