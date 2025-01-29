from flask import Flask, jsonify, request
from flask_cors import CORS
from services.twitter_service import TwitterService
from services.data_cleaning import DataCleaner
from services.sentiment_analysis import SentimentAnalyzer
from config import TwitterConfig

app = Flask(__name__)
cors = CORS(app, origins='*')

# Initialize services
twitter_config = TwitterConfig()
twitter_service = TwitterService(twitter_config)
data_cleaner = DataCleaner()

# Initialize the new sentiment analyzer with model path
sentiment_analyzer = SentimentAnalyzer(
    model_path='services/sentiment_analysis_model.pt',  # Update this path to your model location
    model_name="cardiffnlp/twitter-xlm-roberta-base-sentiment"
)

@app.route("/api/variable", methods=['POST'])
def variable():
    user_input = request.json.get("searchQuery", "")
    
    if not user_input:
        return jsonify({"message": "No search query provided."}), 400
    
    try:
        # Fetch and process data
        df = twitter_service.fetch_tweets(user_input)
        df = data_cleaner.clean_dataframe(df)
        
        # Use new sentiment analyzer but keep same output format
        total, pos_pct, neg_pct, neu_pct = sentiment_analyzer.analyze_dataframe(df)
        
        return jsonify({
            "message": f"Received user input: {user_input}",
            "user_input": user_input,
            "total": total,
            "positive_percentage": pos_pct,
            "negative_percentage": neg_pct,
            "neutral_percentage": neu_pct
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch or process Twitter data"
        }), 500

@app.route("/api/trends", methods=['GET'])
def trends():
    try:
        # Get woeid from query parameters, default to worldwide (1)
        woeid = request.args.get("woeid", "1")
        
        # Fetch trends data
        trends_data = twitter_service.fetch_trends(woeid)
        
        return jsonify({
            "trends": trends_data,
            "total_trends": len(trends_data),
            "woeid": woeid
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch trends data"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=8081)