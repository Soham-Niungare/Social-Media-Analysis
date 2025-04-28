from flask import Blueprint, request, jsonify
from services.data_service import DataCleaner
import logging

logger = logging.getLogger(__name__)

def register_translation_routes(app):
    translation_bp = Blueprint('translation', __name__)
    
    # Initialize services
    data_cleaner = DataCleaner()
    
    @translation_bp.route('/api/translations/<tweet_id>', methods=['GET'])
    def get_translation(tweet_id):
        try:
            translation = data_cleaner.get_translation_for_tweet(tweet_id)
            
            if translation:
                return jsonify({
                    'success': True,
                    'translation': translation
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'No translation found for this tweet'
                }), 404
                
        except Exception as e:
            logger.error(f"Error retrieving translation: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'Error retrieving translation: {str(e)}'
            }), 500
    
    @translation_bp.route('/api/translations', methods=['GET'])
    def list_translations():
        try:
            translations = data_cleaner.translator.get_saved_translations()
            
            return jsonify({
                'success': True,
                'count': len(translations),
                'translations': translations
            })
            
        except Exception as e:
            logger.error(f"Error listing translations: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'Error listing translations: {str(e)}'
            }), 500
    
    app.register_blueprint(translation_bp)