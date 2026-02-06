from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from routes.photos import photos_bp
from routes.chat import chat_bp
from routes.share import share_bp

app = Flask(__name__)

# 🔥 Allow frontend to talk to backend
CORS(app)

# Register routes
app.register_blueprint(photos_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")
app.register_blueprint(share_bp, url_prefix="/api")

# Serve uploaded images
@app.route("/storage/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("storage/images", filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
