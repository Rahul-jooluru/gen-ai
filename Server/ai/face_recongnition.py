from deepface import DeepFace

def extract_faces(image_path):
    """
    Detect faces and return embeddings
    """
    faces = DeepFace.extract_faces(
        img_path=image_path,
        target_size=(160, 160),
        detector_backend="retinaface",
        enforce_detection=False
    )
    return faces


def get_embedding(face_img):
    """
    Generate face embedding
    """
    embedding = DeepFace.represent(
        img_path=face_img,
        model_name="Facenet512",
        enforce_detection=False
    )
    return embedding[0]["embedding"]
