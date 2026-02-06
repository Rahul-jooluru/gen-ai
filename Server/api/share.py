from flask import Blueprint, request, jsonify

share_bp = Blueprint('share', __name__)


@share_bp.route('/', methods=['POST'])
def share_image():
    """Share an image"""
    data = request.get_json()
    
    if not data or 'image_id' not in data:
        return jsonify({"error": "image_id is required"}), 400
    
    # TODO: Implement image sharing logic
    return jsonify({"message": "Image shared successfully"}), 200