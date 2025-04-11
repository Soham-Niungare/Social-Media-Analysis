# server/app.py
from flask import Flask
from flask_cors import CORS
import logging
from api.search_routes import register_search_routes
from api.trends_routes import register_trends_routes
from api.translation_routes import register_translation_routes

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cors = CORS(app, origins='*')

# Register routes
register_search_routes(app)
register_trends_routes(app)
register_translation_routes(app)

if __name__ == "__main__":
    app.run(debug=True, port=8081)