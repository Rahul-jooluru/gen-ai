<<<<<<< HEAD
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
=======
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from db.database import init_db

# API blueprints
from api.upload import upload_bp
from api.search import search_bp
from api.share import share_bp


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Enable CORS (frontend → backend)
    CORS(app, supports_credentials=True)

    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(search_bp, url_prefix="/api/search")
    app.register_blueprint(share_bp, url_prefix="/api/share")

    # Health check
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "service": "Drishyamitra Backend"
        })

    # Global error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(str(e))
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=app.config.get("PORT", 5000),
        debug=app.config.get("DEBUG", True)
    )
>>>>>>> ef490779ceca3245d2ac83b080a7e00b8c0536e5
