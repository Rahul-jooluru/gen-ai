import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    """
    Base configuration (default)
    """

    # -----------------------------
    # Flask
    # -----------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))

    # -----------------------------
    # Database
    # -----------------------------
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # sqlite / postgres
    DB_NAME = os.getenv("DB_NAME", "drishyamitra.db")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "")
    DB_PORT = os.getenv("DB_PORT", "")

    # Set SQLALCHEMY_DATABASE_URI based on DB_TYPE
    _db_type = os.getenv("DB_TYPE", "sqlite")
    if _db_type == "sqlite":
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/{DB_NAME}"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------------
    # Storage Paths
    # -----------------------------
    STORAGE_DIR = BASE_DIR / "storage"
    IMAGE_UPLOAD_DIR = STORAGE_DIR / "images"
    EMBEDDING_DIR = STORAGE_DIR / "embeddings"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit

    # -----------------------------
    # AI / ML
    # -----------------------------
    FACE_MODEL = os.getenv("FACE_MODEL", "facenet")
    FACE_DISTANCE_THRESHOLD = float(
        os.getenv("FACE_DISTANCE_THRESHOLD", 0.6)
    )

    TAGGING_MODEL = os.getenv("TAGGING_MODEL", "clip")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")

    # -----------------------------
    # Security
    # -----------------------------
    PASSWORD_HASH_ALGORITHM = "bcrypt"
    TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", 24))

    # -----------------------------
    # App Metadata
    # -----------------------------
    APP_NAME = "Drishyamitra"
    APP_VERSION = "0.1.0"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False