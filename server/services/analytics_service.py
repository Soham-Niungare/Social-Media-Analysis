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
        self.load_model()  
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
            

        compound = (scores[2] - scores[0]) 
        
        return float(compound)

    @staticmethod
    def classify_sentiment(score: float) -> str:
        if score >= 0.05:
            return 'positive'
        elif score <= -0.05:
            return 'negative'
        return 'neutral'

    def analyze_dataframe(self, df: pd.DataFrame) -> Tuple[int, float, float, float]:
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
    
class EngagementAnalyzer:
    def __init__(self, sentiment_analyzer):
        self.metrics = ['favorite_count', 'retweet_count', 'reply_count']
        self.metric_names = {
            'favorite_count': 'Likes',
            'retweet_count': 'Retweets',
            'reply_count': 'Replies'
        }
        self.sentiment_analyzer = sentiment_analyzer
    
    def format_engagement_metrics(self, df: pd.DataFrame) -> list:
        if 'sentiment' not in df.columns:
            df['sentiment_score'] = df['cleaned_text'].apply(self.sentiment_analyzer.get_sentiment_score)
            df['sentiment'] = df['sentiment_score'].apply(self.sentiment_analyzer.classify_sentiment)
        
        print("DataFrame shape:", df.shape)
        print("Sentiment distribution:", df['sentiment'].value_counts())
        print("Sample of engagement metrics by sentiment:")
        print(df.groupby('sentiment')[self.metrics].mean())

        for metric in self.metrics:
            df[metric] = pd.to_numeric(df[metric], errors='coerce').fillna(0)

        engagement_by_sentiment = df.groupby('sentiment')[self.metrics].mean()

        engagement_dict = engagement_by_sentiment.to_dict()
        
        formatted_metrics = []
        for metric_key in self.metrics:
            metric_data = {
                "metric": self.metric_names[metric_key],
                "positive": round(engagement_dict[metric_key].get('positive', 0), 1),
                "neutral": round(engagement_dict[metric_key].get('neutral', 0), 1),
                "negative": round(engagement_dict[metric_key].get('negative', 0), 1)
            }
            formatted_metrics.append(metric_data)
            
        return formatted_metrics

    def analyze(self, df: pd.DataFrame) -> dict:
        df['sentiment_score'] = df['cleaned_text'].apply(self.sentiment_analyzer.get_sentiment_score)
        df['sentiment'] = df['sentiment_score'].apply(self.sentiment_analyzer.classify_sentiment)
        
        sentiment_counts = df['sentiment'].value_counts()
        total = len(df)
        
        sentiment_analysis = {
            "total": total,
            "positive_percentage": round((sentiment_counts.get('positive', 0) / total) * 100, 1),
            "negative_percentage": round((sentiment_counts.get('negative', 0) / total) * 100, 1),
            "neutral_percentage": round((sentiment_counts.get('neutral', 0) / total) * 100, 1)
        }
        
        engagement_metrics = self.format_engagement_metrics(df)

        print("Engagement metrics to be returned:", engagement_metrics)
        
        return {
            "sentiment_analysis": sentiment_analysis,
            "engagement_metrics": engagement_metrics
        }