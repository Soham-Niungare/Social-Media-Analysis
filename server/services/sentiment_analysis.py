import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from typing import Tuple
import numpy as np
from scipy.special import softmax

class SentimentAnalyzer:
    def __init__(self, model_path='sentiment_analysis_model.pt', model_name="cardiffnlp/twitter-xlm-roberta-base-sentiment"):
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # Load our trained weights
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()  # Set to evaluation mode
        
        # Move to CPU/GPU as available
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.model.to(self.device)

    def preprocess(self, text: str) -> str:
        """Preprocess text similar to training"""
        words = text.split()
        words = ['@user' if word.startswith('@') else word for word in words]
        words = ['http' if word.startswith('http') else word for word in words]
        return ' '.join(words)

    def get_sentiment_score(self, text: str) -> float:
        """Get sentiment score for a single text"""
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
        df['sentiment_score'] = df['cleaned_text'].apply(self.get_sentiment_score)
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