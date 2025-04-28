# server/api/search_routes.py
from flask import jsonify, request, Blueprint
from services.twitter_service import TwitterService
from services.data_service import DataCleaner
from services.analytics_service import SentimentAnalyzer, EngagementAnalyzer
from config.config import TwitterConfig
import json
import os
import datetime
import logging

logger = logging.getLogger(__name__)

# Initialize services
twitter_config = TwitterConfig()
twitter_service = TwitterService(twitter_config)
data_cleaner = DataCleaner()
sentiment_analyzer = SentimentAnalyzer(
    model_path='model/sentiment_analysis_model.pt',
    model_name="cardiffnlp/twitter-xlm-roberta-base-sentiment"
)
engagement_analyzer = EngagementAnalyzer(sentiment_analyzer)


os.makedirs('server/data', exist_ok=True)

os.makedirs('server/data/translations', exist_ok=True)

def save_tweets_with_sentiment(df, search_query):
    available_columns = df.columns.tolist()
    
    desired_columns = ['id', 'text', 'cleaned_text', 'favorite_count', 
                       'retweet_count', 'reply_count', 'sentiment', 'sentiment_score',
                       'original_lang']  
    
    columns_to_save = [col for col in desired_columns if col in available_columns]
    
    tweet_data = df[columns_to_save].copy()
    
    tweet_records = tweet_data.to_dict(orient='records')
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    metadata = {
        "search_query": search_query,
        "timestamp": timestamp,
        "total_tweets": len(tweet_records)
    }
    
    lang_stats = calculate_language_stats(df)
    metadata["language_stats"] = lang_stats["languages"]
    
    data_to_save = {
        "metadata": metadata,
        "tweets": tweet_records
    }
    
    sanitized_query = search_query.replace(" ", "_").replace("/", "_").replace("\\", "_")[:30]
    filename = f"data/tweets_{sanitized_query}_{timestamp}.json"
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    
    with open("data/latest_tweets.json", 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    
    return filename

def calculate_language_stats(df):
    if 'original_lang' not in df.columns:
        return {'languages': []}
        
    lang_counts = df['original_lang'].value_counts().to_dict()
    total = len(df)
    
    languages = []
    for lang, count in lang_counts.items():
        lang_name = 'Hindi' if lang == 'hi' else 'English' if lang == 'en' else lang
        languages.append({
            'language': lang_name,
            'code': lang,
            'count': int(count),
            'percentage': round((count / total) * 100, 1)
        })
        
    return {'languages': languages}

def prepare_tweet_data(df):
    tweet_list = []
    
    for _, row in df.iterrows():
        tweet = {
            'id': row['id'],
            'text': row['text'],
            'cleaned_text': row.get('cleaned_text', row['text']),
            'favorite_count': row.get('favorite_count', 0),
            'retweet_count': row.get('retweet_count', 0),
            'reply_count': row.get('reply_count', 0),
            'sentiment': row.get('sentiment', 'neutral'),
            'sentiment_score': row.get('sentiment_score', 0),
            'original_lang': row.get('original_lang', 'en'),
            'has_translation': row.get('original_lang', 'en') != 'en'
        }
        
        tweet_list.append(tweet)
        
    return tweet_list

def register_search_routes(app):
    search_bp = Blueprint('search', __name__)

    @search_bp.route("/api/variable", methods=['POST'])
    def variable():
        user_input = request.json.get("searchQuery", "")
        if not user_input:
            return jsonify({"message": "No search query provided."}), 400
        try:
            df = twitter_service.fetch_tweets(user_input)
            
            df = data_cleaner.clean_dataframe(df, user_input)
            
            analysis_results = engagement_analyzer.analyze(df)
            
            lang_stats = calculate_language_stats(df)
            
            tweet_data = prepare_tweet_data(df)
            
            filename = save_tweets_with_sentiment(df, user_input)
            
            response = {
                "sentiment_analysis": analysis_results.get('sentiment_analysis', {}),
                "engagement_metrics": analysis_results.get('engagement_metrics', {}),
                "tweets_data": {
                    "filename": os.path.basename(filename),
                    "count": len(df),
                    "search_query": user_input
                }
            }
            
            print("Final API Response:", response)
            return jsonify(response)
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            print(f"Error occurred: {str(e)}")  # Debug log
            return jsonify({
                "error": str(e),
                "message": "Failed to fetch or process Twitter data"
            }), 500
    
    @search_bp.route("/api/tweets", methods=['GET'])
    def get_latest_tweets():
        try:
            with open("server/data/latest_tweets.json", 'r', encoding='utf-8') as f:
                tweet_data = json.load(f)
            return jsonify(tweet_data)
        except FileNotFoundError:
            return jsonify({"message": "No tweet data available yet"}), 404
        except Exception as e:
            logger.error(f"Error retrieving tweet data: {str(e)}")
            print(f"Error retrieving tweet data: {str(e)}")
            return jsonify({
                "error": str(e),
                "message": "Failed to retrieve tweet data"
            }), 500
    
    @search_bp.route("/api/translations/<tweet_id>", methods=['GET'])
    def get_translation(tweet_id):
        try:
            translation_file = f"server/data/translations/{tweet_id}.json"
            if not os.path.exists(translation_file):
                return jsonify({"message": "Translation not available"}), 404
                
            with open(translation_file, 'r', encoding='utf-8') as f:
                translation_data = json.load(f)
            return jsonify(translation_data)
        except Exception as e:
            logger.error(f"Error retrieving translation: {str(e)}")
            return jsonify({
                "error": str(e),
                "message": "Failed to retrieve translation"
            }), 500
    
    @search_bp.route("/api/translations", methods=['GET'])
    def list_translations():
        try:
            translations_dir = "server/data/translations"
            if not os.path.exists(translations_dir):
                return jsonify({"translations": []})
                
            translation_files = [f[:-5] for f in os.listdir(translations_dir) if f.endswith('.json')]
            return jsonify({"translations": translation_files})
        except Exception as e:
            logger.error(f"Error listing translations: {str(e)}")
            return jsonify({
                "error": str(e),
                "message": "Failed to list translations"
            }), 500
    
    app.register_blueprint(search_bp)