import json
from flask import Blueprint, request, jsonify

chat_bp = Blueprint("chat", __name__)

DATA_FILE = "data/photos.json"

def load_photos():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "")

    # Simple search implementation
    photos = load_photos()
    
    # Basic filtering based on query
    results = []
    query_lower = query.lower()
    
    for photo in photos:
        tags = [tag.lower() for tag in photo.get("tags", [])]
        if any(word in tags for word in query_lower.split()):
            results.append(photo)
    
    return jsonify({
        "response": f"Found {len(results)} photos matching your query",
        "photos": results
    })
