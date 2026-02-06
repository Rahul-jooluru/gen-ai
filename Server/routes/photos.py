import os
import json
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ai.image_tagging import generate_tags

photos_bp = Blueprint("photos", __name__)

DATA_FILE = "data/photos.json"
UPLOAD_DIR = "storage/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
        return jsonify(load_photos())
    except Exception as e:
        print("GET PHOTOS ERROR:", e)
        return jsonify([])


@photos_bp.route("/upload", methods=["POST"])
def upload_photo():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    if image.filename == "" or not allowed_file(image.filename):
        return jsonify({"error": "Invalid file type"}), 400

    photo_id = str(uuid.uuid4())
    safe_name = secure_filename(image.filename)
    filename = f"{photo_id}_{safe_name}"
    path = os.path.join(UPLOAD_DIR, filename)

    image.save(path)

    # 🔥 AI TAGGING
    try:
        tags = generate_tags(path)
        print(f"✅ Tags generated: {tags}")
    except Exception as e:
        print(f"❌ TAGGING ERROR: {str(e)}")
        print(f"   Image path: {path}")
        tags = []

    base_url = request.host_url.rstrip("/")

    photo = {
        "id": photo_id,
        "url": f"{base_url}/storage/images/{filename}",
        "tags": tags,
        "date": datetime.utcnow().isoformat()
    }

    photos = load_photos()
    photos.append(photo)
    save_photos(photos)

    return jsonify(photo), 201


@photos_bp.route("/photos/<photo_id>", methods=["DELETE"])
def delete_photo(photo_id):
    photos = load_photos()
    remaining = []

    for p in photos:
        if p["id"] == photo_id:
            # delete image file
            filename = p.get("url", "").split("/")[-1]
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            remaining.append(p)

    save_photos(remaining)
    return jsonify({"status": "deleted"}), 200
