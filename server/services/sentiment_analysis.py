import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from typing import Tuple
import numpy as np
from scipy.special import softmax

class SentimentAnalyzer:
    def __init__(self, model_path= None, model_name=None):
        self.model_path = model_path
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def load_model(self):
        if self.model is None or self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.load_state_dict(torch.load(self.model_path))
            self.model.eval()
            self.model = self.model.to(self.device)

    def preprocess(self, text: str) -> str:
        """Preprocess text similar to training"""
        words = text.split()
        words = ['@user' if word.startswith('@') else word for word in words]
        words = ['http' if word.startswith('http') else word for word in words]
        return ' '.join(words)

    def get_sentiment_score(self, text: str) -> float:
        """Get sentiment score for a single text"""
        self.load_model()  # Load model only when needed
        # Preprocess text
        text = self.preprocess(text)
        
        # Tokenize
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=128)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = outputs.logits[0].cpu().numpy()
            scores = softmax(scores)
            
        # Convert to compound score similar to VADER (-1 to 1 range)
        # Assuming scores[0] is negative, scores[1] is neutral, scores[2] is positive
        compound = (scores[2] - scores[0]) # Will be between -1 and 1
        
        return float(compound)

    @staticmethod
    def classify_sentiment(score: float) -> str:
        """Classify sentiment based on compound score"""
        if score >= 0.05:
            return 'positive'
        elif score <= -0.05:
            return 'negative'
        return 'neutral'

    def analyze_dataframe(self, df: pd.DataFrame) -> Tuple[int, float, float, float]:
        """Analyze sentiment for entire dataframe"""
        # Process in batches for efficiency
        df = self.analyze_text_batch(df['cleaned_text'].tolist())
        df['sentiment'] = df['sentiment_score'].apply(self.classify_sentiment)

        sentiment_counts = df['sentiment'].value_counts()
        total = len(df)
        
        return (
            total,
            (sentiment_counts.get('positive', 0) / total) * 100,
            (sentiment_counts.get('negative', 0) / total) * 100,
            (sentiment_counts.get('neutral', 0) / total) * 100
        )

    def analyze_text_batch(self, texts: list) -> pd.DataFrame:
        """Analyze a batch of texts and return detailed results"""
        # Preprocess all texts
        processed_texts = [self.preprocess(text) for text in texts]
        
        # Tokenize
        inputs = self.tokenizer(processed_texts, return_tensors='pt', padding=True, truncation=True, max_length=128)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get predictions
        results = []
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = outputs.logits.cpu().numpy()
            scores = softmax(scores, axis=1)
            
            for text, score in zip(texts, scores):
                compound = score[2] - score[0]  # Positive - Negative
                sentiment = self.classify_sentiment(compound)
                results.append({
                    'text': text,
                    'sentiment': sentiment,
                    'score': compound,
                    'negative_prob': score[0],
                    'neutral_prob': score[1],
                    'positive_prob': score[2]
                })
        
        return pd.DataFrame(results)