from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from apify_client import ApifyClient

app = Flask(__name__)
cors = CORS(app, origins='*')



@app.route("/api/variable", methods=['POST'])
def variable():
    user_input = request.json.get("searchQuery", "")
    
    if not user_input:
        return jsonify({
            "message": "No search query provided."
        }), 400
    
    total, positive_percentage, negative_percentage, neutral_percentage = fetch_data_from_apify(user_input)

    return jsonify({
        "message": f"Received user input: {user_input}",
        "user_input": user_input,
        "total": total,
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage,
        "neutral_percentage": neutral_percentage
    })

def fetch_data_from_apify(query):
    client = ApifyClient("apify_api_lX3pUredBtOxqhHaH2bWwHnaXbGbCM2C7V64")
    print("Apify client configured")

    run_input = {
        "startUrls": [],
        "handles": [],
        "userQueries": [query], 
        "tweetsDesired": 100,
        "profilesDesired": 10,
        "withReplies": True,
        "includeUserInfo": True,
        "proxyConfig": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }
    print("Running Apify Actor...")

    run = client.actor("VsTreSuczsXhhRIqa").call(run_input=run_input)

    data_list = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        data_list.append(item)

    df = pd.DataFrame(data_list)

    df.to_csv('fetched_tweets.csv', index=False)
    print("Fetched data saved to 'fetched_tweets.csv'")

    data = pd.read_csv('fetched_tweets.csv')
    relevant_columns = ['id', 'text', 'timestamp', 'likes']
    data_cleaned = data[relevant_columns]
    print(data_cleaned.info())
    
    data_cleaned = data_cleaned.dropna(subset=['text'])
    data_cleaned = data_cleaned[data_cleaned['text'].str.strip().astype(bool)]

    def preprocess_tweet(tweet):
        tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
        tweet = re.sub(r'@\w+|#\w+', '', tweet)
        tweet = re.sub(r'\W+', ' ', tweet)
        tweet = tweet.lower()
        return tweet

    data_cleaned['cleaned_text'] = data_cleaned['text'].apply(preprocess_tweet)

    data_cleaned.to_csv('cleaned_tweet_dataset.csv', index=False)
    print("Cleaned data saved to 'cleaned_tweet_dataset.csv'")

    # Perform Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()
    
    def get_sentiment_score(tweet):
        score = analyzer.polarity_scores(tweet)
        return score['compound']

    data_cleaned['sentiment_score'] = data_cleaned['cleaned_text'].apply(get_sentiment_score)

    def classify_sentiment(score):
        if score >= 0.05:
            return 'positive'
        elif score <= -0.05:
            return 'negative'
        else:
            return 'neutral'

    data_cleaned['sentiment'] = data_cleaned['sentiment_score'].apply(classify_sentiment)

    sentiment_counts = data_cleaned['sentiment'].value_counts()
    total = len(data_cleaned)
    positive_percentage = (sentiment_counts.get('positive', 0) / total) * 100
    negative_percentage = (sentiment_counts.get('negative', 0) / total) * 100
    neutral_percentage = (sentiment_counts.get('neutral', 0) / total) * 100

    print(f"Positive Sentiment: {positive_percentage:.2f}%")
    print(f"Negative Sentiment: {negative_percentage:.2f}%")
    print(f"Neutral Sentiment: {neutral_percentage:.2f}%")

    return total, positive_percentage, negative_percentage, neutral_percentage

if __name__ == "__main__":
    app.run(debug=True, port=8081)
