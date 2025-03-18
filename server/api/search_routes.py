# server/api/search_routes.py
from flask import jsonify, request
from services.twitter_service import TwitterService
from services.data_service import DataCleaner
from services.analytics_service import SentimentAnalyzer, EngagementAnalyzer
from config.config import TwitterConfig
import json
import os
import datetime

# Initialize services
twitter_config = TwitterConfig()
twitter_service = TwitterService(twitter_config)
data_cleaner = DataCleaner()
sentiment_analyzer = SentimentAnalyzer(
    model_path='models/sentiment_analysis_model.pt',
    model_name="cardiffnlp/twitter-xlm-roberta-base-sentiment"
)
engagement_analyzer = EngagementAnalyzer(sentiment_analyzer)

# Create directory for storing tweet data files if it doesn't exist
os.makedirs('server/data', exist_ok=True)

def save_tweets_with_sentiment(df, search_query):
    """Save the tweets with their sentiment analysis to a JSON file"""
    # Get the columns that are available in the DataFrame
    available_columns = df.columns.tolist()
    
    # Define the columns we want to save, if they exist
    desired_columns = ['id', 'text', 'cleaned_text', 'favorite_count', 
                       'retweet_count', 'reply_count', 'sentiment', 'sentiment_score']
    
    # Filter to only include columns that exist in the DataFrame
    columns_to_save = [col for col in desired_columns if col in available_columns]
    
    # Create a subset of the dataframe with only the columns we want to keep
    tweet_data = df[columns_to_save].copy()
    
    # Convert to dictionary records
    tweet_records = tweet_data.to_dict(orient='records')
    
    # Create metadata
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    metadata = {
        "search_query": search_query,
        "timestamp": timestamp,
        "total_tweets": len(tweet_records)
    }
    
    # Create the final data structure
    data_to_save = {
        "metadata": metadata,
        "tweets": tweet_records
    }
    
    # Save to file with query name and timestamp
    sanitized_query = search_query.replace(" ", "_").replace("/", "_").replace("\\", "_")[:30]
    filename = f"server/data/tweets_{sanitized_query}_{timestamp}.json"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    
    # Always update a "latest.json" file to have the most recent search results
    with open("server/data/latest_tweets.json", 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    
    return filename

def register_search_routes(app):
    @app.route("/api/variable", methods=['POST'])
    def variable():
        user_input = request.json.get("searchQuery", "")
        if not user_input:
            return jsonify({"message": "No search query provided."}), 400
        try:
            # Fetch and process data
            df = twitter_service.fetch_tweets(user_input)
            df = data_cleaner.clean_dataframe(df)
            
            # Get integrated analysis
            analysis_results = engagement_analyzer.analyze(df)
            
            # Save tweets with sentiment to file
            filename = save_tweets_with_sentiment(df, user_input)
            
            # Add file information to the response
            analysis_results["tweets_data"] = {
                "filename": os.path.basename(filename),
                "count": len(df),
                "search_query": user_input
            }
            
            # Debug print final response
            print("Final API Response:", analysis_results)
            return jsonify(analysis_results)
        except Exception as e:
            print(f"Error occurred: {str(e)}")  # Debug log
            return jsonify({
                "error": str(e),
                "message": "Failed to fetch or process Twitter data"
            }), 500
    
    @app.route("/api/tweets", methods=['GET'])
    def get_latest_tweets():
        """Endpoint to retrieve the latest saved tweets"""
        try:
            with open("server/data/latest_tweets.json", 'r', encoding='utf-8') as f:
                tweet_data = json.load(f)
            return jsonify(tweet_data)
        except FileNotFoundError:
            return jsonify({"message": "No tweet data available yet"}), 404
        except Exception as e:
            print(f"Error retrieving tweet data: {str(e)}")
            return jsonify({
                "error": str(e),
                "message": "Failed to retrieve tweet data"
            }), 500