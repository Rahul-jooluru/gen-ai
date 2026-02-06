from flask import Blueprint, request, jsonify

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/', methods=['POST'])
def upload_image():
    """Handle image upload"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # TODO: Implement image upload logic
    return jsonify({"message": "File uploaded successfully"}), 200