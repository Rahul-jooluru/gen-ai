from flask import Flask, send_from_directory
from flask_cors import CORS

from routes.photos import photos_bp
from routes.chat import chat_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(photos_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")

@app.route("/storage/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("storage/images", filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
