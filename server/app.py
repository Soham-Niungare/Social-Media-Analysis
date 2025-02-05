from flask import Flask, jsonify, request
from flask_cors import CORS
from services.engagement_analysis import EngagementAnalyzer
from services.twitter_service import TwitterService
from services.data_cleaning import DataCleaner
from services.sentiment_analysis import SentimentAnalyzer
from config import TwitterConfig
from countries import COUNTRIES_WOEID
import logging

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
engagement_analyzer = EngagementAnalyzer(sentiment_analyzer)

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

        # Debug print final response
        print("Final API Response:", analysis_results)
        
        return jsonify(analysis_results)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug log
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch or process Twitter data"
        }), 500

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route("/api/trends", methods=['GET'])
def trends():
    try:
        country = request.args.get("country", "Worldwide")

        # Get the corresponding WOEID
        woeid = COUNTRIES_WOEID.get(country, 1)  # Defaults to Worldwide if not found
        
        # Log the request
        logger.debug(f"Received trends request for woeid: {woeid}")
        
        # Fetch trends data
        trends_data = twitter_service.fetch_trends(woeid)
        
        # Log the trends data before sending
        logger.debug(f"Fetched trends data: {trends_data}")

        # Limit trends to 25 (can adjust as needed)
        limited_trends = trends_data[:25]

        
        # Create the response
        response_data = {
            "country": country,
            "trends": trends_data,
            "total_trends": len(limited_trends),
            "woeid": woeid
        }
        
        # Log the final response
        logger.debug(f"Sending response: {response_data}")
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in trends endpoint: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch trends data"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=8081)