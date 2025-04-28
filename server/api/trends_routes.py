# server/api/trends_routes.py
from flask import jsonify, request
import logging
from services.twitter_service import TwitterService
from config.config import TwitterConfig
from config.constants import COUNTRIES_WOEID

# Initialize services
twitter_config = TwitterConfig()
twitter_service = TwitterService(twitter_config)


logger = logging.getLogger(__name__)

def register_trends_routes(app):
    @app.route("/api/trends", methods=['GET'])
    def trends():
        try:
            country = request.args.get("country", "Worldwide")

            woeid = COUNTRIES_WOEID.get(country, 1)  

            logger.debug(f"Received trends request for woeid: {woeid}")

            trends_data = twitter_service.fetch_trends(woeid)

            logger.debug(f"Fetched trends data: {trends_data}")

            limited_trends = trends_data[:25]

            response_data = {
                "country": country,
                "trends": trends_data,
                "total_trends": len(limited_trends),
                "woeid": woeid
            }

            logger.debug(f"Sending response: {response_data}")
            return jsonify(response_data)
        except Exception as e:
            logger.error(f"Error in trends endpoint: {str(e)}")
            return jsonify({
                "error": str(e),
                "message": "Failed to fetch trends data"
            }), 500