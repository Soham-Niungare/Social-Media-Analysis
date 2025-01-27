from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import json

app = Flask(__name__)
cors = CORS(app, origins='*')

def fetch_twitter_data(query):
    url = "https://twitter154.p.rapidapi.com/search/search"
    
    querystring = {
        "query": query,
        "section": "latest",
        "min_retweets": "1",
        "min_likes": "1",
        "limit": "50",
        "language": "en"
    }
    
    headers = {
        "x-rapidapi-key": "6c80c82d04mshcc770f8485ad426p1f8822jsn04464e6a0a17",
        "x-rapidapi-host": "twitter154.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Debug: Print the first result to see the structure
    print("First tweet structure:", json.dumps(data.get("results", [])[0] if data.get("results") else "No results", indent=2))
    
    # Convert API response to DataFrame
    tweets_data = []
    for tweet in data.get("results", []):
        tweet_data = {
            "id": tweet.get("tweet_id"),
            "text": tweet.get("tweet_text", tweet.get("text", "")),  # Try both possible field names
            "timestamp": tweet.get("creation_date"),
            "likes": tweet.get("favorite_count")
        }
        print("Processed tweet data:", tweet_data)  # Debug print
        tweets_data.append(tweet_data)
    
    if not tweets_data:
        raise Exception("No tweets found in the response")
    
    df = pd.DataFrame(tweets_data)
    print("DataFrame head:", df.head())  # Debug print
    print("DataFrame info:", df.info())  # Debug print
    
    # Clean and preprocess the data
    df = df.dropna(subset=['text'])
    df = df[df['text'].str.strip().astype(bool)]
    
    def preprocess_tweet(tweet):
        if not isinstance(tweet, str):
            print(f"Warning: non-string tweet encountered: {tweet}")
            tweet = str(tweet)
        tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
        tweet = re.sub(r'@\w+|#\w+', '', tweet)
        tweet = re.sub(r'\W+', ' ', tweet)
        tweet = tweet.lower()
        return tweet
    
    df['cleaned_text'] = df['text'].apply(preprocess_tweet)
    
    # Perform Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()
    
    def get_sentiment_score(tweet):
        score = analyzer.polarity_scores(tweet)
        return score['compound']
    
    df['sentiment_score'] = df['cleaned_text'].apply(get_sentiment_score)
    
    def classify_sentiment(score):
        if score >= 0.05:
            return 'positive'
        elif score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    df['sentiment'] = df['sentiment_score'].apply(classify_sentiment)
    
    # Calculate sentiment percentages
    sentiment_counts = df['sentiment'].value_counts()
    total = len(df)
    positive_percentage = (sentiment_counts.get('positive', 0) / total) * 100
    negative_percentage = (sentiment_counts.get('negative', 0) / total) * 100
    neutral_percentage = (sentiment_counts.get('neutral', 0) / total) * 100
    
    # Save processed data for debugging
    df.to_csv('processed_tweets.csv', index=False)
    
    return total, positive_percentage, negative_percentage, neutral_percentage

@app.route("/api/variable", methods=['POST'])
def variable():
    user_input = request.json.get("searchQuery", "")
    
    if not user_input:
        return jsonify({
            "message": "No search query provided."
        }), 400
    
    try:
        print(f"Processing search query: {user_input}")  # Debug print
        total, positive_percentage, negative_percentage, neutral_percentage = fetch_twitter_data(user_input)
        
        return jsonify({
            "message": f"Received user input: {user_input}",
            "user_input": user_input,
            "total": total,
            "positive_percentage": positive_percentage,
            "negative_percentage": negative_percentage,
            "neutral_percentage": neutral_percentage
        })
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug print
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch or process Twitter data"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=8081)