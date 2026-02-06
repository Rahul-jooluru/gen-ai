import os
import json
import uuid
from flask import Blueprint, request, jsonify

photos_bp = Blueprint("photos", __name__)

DATA_FILE = "data/photos.json"
UPLOAD_DIR = "storage/images"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

def load_photos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_photos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@photos_bp.route("/photos", methods=["GET"])
def get_photos():
    try:
        photos = load_photos()
        return jsonify(photos)
    except:
        return jsonify([])

@photos_bp.route("/upload", methods=["POST"])
def upload_photo():
    if "image" not in request.files:
        return jsonify({"error": "No image"}), 400

    image = request.files["image"]
    photo_id = str(uuid.uuid4())
    filename = f"{photo_id}_{image.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    image.save(path)

    photos = load_photos()

    photo = {
        "id": photo_id,
        "url": f"http://localhost:5000/storage/images/{filename}",
        "tags": [],
        "date": None
    }

    photos.append(photo)
    save_photos(photos)

    return jsonify(photo), 201

@photos_bp.route("/photos/<photo_id>", methods=["DELETE"])
def delete_photo(photo_id):
    photos = load_photos()
    photos = [p for p in photos if p["id"] != photo_id]
    save_photos(photos)
    return jsonify({"status": "deleted"}), 200
