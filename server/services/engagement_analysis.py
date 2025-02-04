import pandas as pd

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
        """Format engagement metrics in the desired structure"""
        # First, add sentiment to each tweet
        if 'sentiment' not in df.columns:
            df['sentiment_score'] = df['cleaned_text'].apply(self.sentiment_analyzer.get_sentiment_score)
            df['sentiment'] = df['sentiment_score'].apply(self.sentiment_analyzer.classify_sentiment)
        
        # Debug print
        print("DataFrame shape:", df.shape)
        print("Sentiment distribution:", df['sentiment'].value_counts())
        print("Sample of engagement metrics by sentiment:")
        print(df.groupby('sentiment')[self.metrics].mean())

        # Ensure metrics are numeric
        for metric in self.metrics:
            df[metric] = pd.to_numeric(df[metric], errors='coerce').fillna(0)

        # Group by sentiment and calculate mean of engagement metrics
        engagement_by_sentiment = df.groupby('sentiment')[self.metrics].mean()

        # Convert the means to a regular dictionary for easier handling
        engagement_dict = engagement_by_sentiment.to_dict()
        
        # Format metrics into the desired structure
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
        """Perform sentiment and engagement analysis"""
        # Add sentiment analysis
        df['sentiment_score'] = df['cleaned_text'].apply(self.sentiment_analyzer.get_sentiment_score)
        df['sentiment'] = df['sentiment_score'].apply(self.sentiment_analyzer.classify_sentiment)
        
        # Calculate sentiment percentages
        sentiment_counts = df['sentiment'].value_counts()
        total = len(df)
        
        sentiment_analysis = {
            "total": total,
            "positive_percentage": round((sentiment_counts.get('positive', 0) / total) * 100, 1),
            "negative_percentage": round((sentiment_counts.get('negative', 0) / total) * 100, 1),
            "neutral_percentage": round((sentiment_counts.get('neutral', 0) / total) * 100, 1)
        }
        
        # Get engagement metrics in the new format
        engagement_metrics = self.format_engagement_metrics(df)

        # Debug print to verify data before return
        print("Engagement metrics to be returned:", engagement_metrics)
        
        return {
            "sentiment_analysis": sentiment_analysis,
            "engagement_metrics": engagement_metrics
        }