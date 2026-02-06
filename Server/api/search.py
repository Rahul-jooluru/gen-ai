from flask import Blueprint, request, jsonify

search_bp = Blueprint('search', __name__)


@search_bp.route('/', methods=['GET'])
def search_images():
    """Search images by query"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    # TODO: Implement image search logic
    return jsonify({"results": []}), 200